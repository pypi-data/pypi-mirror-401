"""Search services for Django models."""

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

from django.apps import apps
from django.conf import settings as django_settings
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI

from .conf import ChatSettings, is_model_allowed

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SearchMatch:
    model_label: str
    display: str


class SQLDatabaseChainSearchService:
    """Search across the database using a SQL agent."""

    def __init__(self, settings: ChatSettings, max_results: int = 10) -> None:
        if settings.provider != "openai":
            raise ValueError("Unsupported provider: %s" % settings.provider)
        if not settings.api_key:
            raise ValueError("DJANGO_AI_ADMIN_CHAT_API_KEY is required for SQL agent.")
        self.settings = settings
        self.max_results = max_results
        self._latest_context = ""
        self._latest_sql_query = None
        self._latest_raw_sql_results = None
        self._db = self._build_database()
        self._llm = ChatOpenAI(
            api_key=settings.api_key,
            model=settings.model,
            temperature=0,
            max_tokens=settings.max_tokens,
        )
        custom_prefix = """You are an expert SQL agent working with a {dialect} database.
Your task is to answer user questions by querying the database and providing clear, natural language responses.
If a question does NOT require database data, answer directly without generating or running any SQL.

IMPORTANT: When comparing text values (strings) in WHERE clauses, ALWAYS use case-insensitive comparisons.
- Use LOWER() function on both sides of the comparison: LOWER(column_name) = LOWER('value')
- For example: WHERE LOWER(registration_number) = LOWER('KA90048') instead of WHERE registration_number = 'KA90048'
- This ensures that searches work regardless of the case of the input value or stored data.

SQL GENERATION RULES:
- ALWAYS end your SQL queries with a semicolon (;)
- NEVER wrap SQL queries in markdown code blocks (no ```sql or ```)
- When generating SQL, output ONLY the raw SQL query
- ALWAYS wrap table names in double quotes: "table_name" instead of table_name
- Example of correct format: SELECT * FROM "RentCars_cars" WHERE id = 1;
- Example of WRONG format: SELECT * FROM RentCars_cars WHERE id = 1;
- Example of WRONG format: ```sql\nSELECT * FROM table_name;\n```

RESPONSE FORMAT:
- After executing the SQL query and getting results, provide a clear, natural language answer
- Summarize the findings in a user-friendly way
- Include relevant details from the query results
- Do NOT include the SQL query in your final answer - only provide the answer based on the results

Always limit your results to {top_k} rows unless the user specifically requests more.
Only use SELECT statements - never use INSERT, UPDATE, DELETE, DROP, or other modifying statements.
Be precise and efficient with your queries."""

        if not create_sql_agent:
            raise ImportError("SQL tooling is unavailable. Install langchain with SQL agent support.")
        toolkit = SQLDatabaseToolkit(db=self._db, llm=self._llm)
        self._agent = create_sql_agent(
            llm=self._llm,
            toolkit=toolkit,
            prefix=custom_prefix,
            verbose=False,
            agent_executor_kwargs={
                "return_intermediate_steps": True,
                "handle_parsing_errors": True,
            },
        )

    def search(self, query: str, chat_history: list[dict] | None = None) -> list[SearchMatch]:
        self._latest_context = ""
        self._latest_sql_query = None
        self._latest_raw_sql_results = None

        if not query:
            self._latest_context = "No matching data found in the database."
            self._latest_sql_query = None
            self._latest_raw_sql_results = None
            return []

        try:
            if hasattr(self._db, "_table_info_cache"):
                self._db._table_info_cache = {}
            if hasattr(self._db, "refresh_table_info"):
                self._db.refresh_table_info()
        except Exception as e:
            logger.debug("Could not refresh database schema cache: %s", e)

        # Build input with chat history context
        input_text = self._build_input_with_history(query, chat_history)

        try:
            result = self._agent.invoke({"input": input_text})
        except Exception as exc:
            logger.exception("Error invoking SQL agent: %s", exc)
            self._latest_context = "No matching data found in the database."
            return []
        print(result)
        intermediate_steps = []
        if isinstance(result, dict):
            intermediate_steps = result.get("intermediate_steps", []) or []
            results_str = str(result.get("output", result.get("result", "")) or "").strip()
        else:
            results_str = str(result or "").strip()

        self._latest_sql_query = self._extract_sql_from_steps(intermediate_steps)
        self._latest_raw_sql_results = self._extract_raw_results_from_steps(intermediate_steps)
        # Clean the output to ensure it's a natural language answer, not SQL
        cleaned_answer = self._clean_answer_from_sql(results_str)
        self._latest_context = cleaned_answer or "No matching data found in the database."
        return []

    def build_context(self, matches: list[SearchMatch]) -> str:
        return self._latest_context or "No matching data found in the database."

    def get_latest_sql_query(self) -> str | None:
        """Return the most recently generated SQL query or None if not available."""
        return self._clean_sql_query(self._latest_sql_query) if self._latest_sql_query else None

    def get_raw_sql_results(self) -> list[dict] | str | None:
        """Return raw SQL results captured from the agent, if any."""
        return self._latest_raw_sql_results

    def _clean_sql_query(self, sql: str) -> str:
        """Clean SQL query from markdown code blocks and extra whitespace."""
        if not sql:
            return ""

        sql = sql.strip()
        code_block_pattern = r"```(?:sql)?\s*\n?(.*?)```"
        matches = re.findall(code_block_pattern, sql, re.DOTALL | re.IGNORECASE)
        if matches:
            sql = matches[0].strip()
        return sql.rstrip(";").strip()

    def _clean_answer_from_sql(self, answer: str) -> str:
        """Remove SQL queries from the answer, keeping only the natural language response."""
        if not answer:
            return ""
        
        # Remove SQL code blocks (```sql ... ```)
        answer = re.sub(r"```(?:sql)?\s*\n?.*?```", "", answer, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove standalone SQL queries that appear as complete statements
        # Pattern: SELECT ... FROM ... WHERE ... ; (multi-line SQL)
        sql_pattern = r"(?i)(?:^|\n)\s*(?:SELECT|WITH|INSERT|UPDATE|DELETE)\s+.*?;\s*(?=\n|$)"
        answer = re.sub(sql_pattern, "", answer, flags=re.DOTALL | re.MULTILINE)
        
        # Clean up extra whitespace
        answer = re.sub(r"\n\s*\n\s*\n", "\n\n", answer)
        answer = answer.strip()
        
        return answer

    def _extract_sql_from_steps(self, steps: list) -> str | None:
        for step in steps:
            if isinstance(step, dict):
                sql_candidate = step.get("query") or step.get("sql") or step.get("sql_query") or step.get("statement")
                if sql_candidate:
                    return self._clean_sql_query(str(sql_candidate))
            if isinstance(step, (list, tuple)) and step:
                action = step[0]
                tool_input = getattr(action, "tool_input", None)
                if isinstance(tool_input, dict):
                    sql_candidate = tool_input.get("query") or tool_input.get("sql") or tool_input.get("statement")
                    if sql_candidate:
                        return self._clean_sql_query(str(sql_candidate))
                if isinstance(tool_input, str) and tool_input.strip().upper().startswith(("SELECT", "WITH")):
                    return self._clean_sql_query(tool_input)
                if isinstance(action, str) and action.strip().upper().startswith(("SELECT", "WITH")):
                    return self._clean_sql_query(action)
        return None

    def _extract_raw_results_from_steps(self, steps: list) -> list[dict] | str | None:
        for step in steps:
            if isinstance(step, (list, tuple)) and len(step) >= 2:
                action, observation = step[0], step[1]
                tool_name = getattr(action, "tool", "") if action is not None else ""
                if isinstance(tool_name, str) and "sql" not in tool_name.lower() and "query" not in tool_name.lower():
                    continue
                if isinstance(observation, (dict, list)):
                    return observation
                if isinstance(observation, str) and observation.strip():
                    return observation.strip()
        return None

    def _build_input_with_history(self, query: str, chat_history: list[dict] | None) -> str:
        """Build input text for SQL agent including chat history context."""
        if not chat_history:
            return query
        
        # Format chat history as context
        history_context_parts = []
        for msg in chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "").strip()
            if not content:
                continue
            
            if role == "user":
                history_context_parts.append(f"User: {content}")
            elif role == "assistant":
                history_context_parts.append(f"Assistant: {content}")
        
        if history_context_parts:
            history_text = "\n".join(history_context_parts)
            return f"""Previous conversation context:
{history_text}

Current question: {query}"""
        
        return query

    def _build_database(self) -> SQLDatabase:
        db_settings = django_settings.DATABASES.get("default", {})
        uri = self._build_sqlalchemy_uri(db_settings)
        include_tables = self._resolve_allowed_tables()
        return SQLDatabase.from_uri(uri, include_tables=include_tables)

    def _resolve_allowed_tables(self) -> list[str] | None:
        models = apps.get_models()
        allowed_tables: list[str] = []
        for model in models:
            if model._meta.abstract or model._meta.proxy:
                continue
            if not is_model_allowed(model._meta.label, self.settings):
                continue
            allowed_tables.append(model._meta.db_table)
        return allowed_tables or None

    def _build_sqlalchemy_uri(self, db_settings: dict) -> str:
        engine = db_settings.get("ENGINE", "")
        name = db_settings.get("NAME", "")
        user = quote_plus(db_settings.get("USER", "") or "")
        password = quote_plus(db_settings.get("PASSWORD", "") or "")
        host = db_settings.get("HOST", "")
        port = db_settings.get("PORT", "")

        if "sqlite3" in engine:
            if name == ":memory:":
                return "sqlite:///:memory:"
            db_path = Path(name)
            if not db_path.is_absolute():
                db_path = Path(django_settings.BASE_DIR) / db_path
            return f"sqlite:///{db_path}"

        if "postgresql" in engine:
            scheme = "postgresql"
        elif "mysql" in engine:
            scheme = "mysql"
        elif "oracle" in engine:
            scheme = "oracle"
        else:
            raise ValueError(f"Unsupported database engine: {engine}")

        auth = f"{user}:{password}@" if user or password else ""
        host_part = host or "localhost"
        port_part = f":{port}" if port else ""
        return f"{scheme}://{auth}{host_part}{port_part}/{name}"

