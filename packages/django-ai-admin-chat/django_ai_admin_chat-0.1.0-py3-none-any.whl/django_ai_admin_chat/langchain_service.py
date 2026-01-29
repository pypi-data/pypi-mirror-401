"""LangChain integration for admin chat."""

from typing import Iterable, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .conf import ChatSettings


class TokenUsage:
    """Class storing token usage information."""

    def __init__(
        self,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
    ):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


class LangChainChatService:
    """Handle chat interactions via LangChain."""

    def __init__(self, settings: ChatSettings) -> None:
        if settings.provider != "openai":
            raise ValueError("Unsupported provider: %s" % settings.provider)
        if not settings.api_key:
            raise ValueError("DJANGO_AI_ADMIN_CHAT_API_KEY is required for OpenAI.")
        self.settings = settings
        self.client = ChatOpenAI(
            api_key=settings.api_key,
            model=settings.model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )

    def chat(self, question: str, context: str, history: list[dict]) -> tuple[str, TokenUsage]:
        """
        Send a query to the model and return the response along with token information.

        Args:
            question: User's question
            context: Database context (can be empty if has_database_context is False)
            history: Chat history
            has_database_context: Whether the context contains database data

        Returns:
            tuple[str, TokenUsage]: Text response and token information
        """
        messages = [SystemMessage(content=self._build_system_prompt(context))]
        for item in history:
            role = item.get("role")
            content = item.get("content", "")
            if not content:
                continue
            if role == "assistant":
                messages.append(AIMessage(content=content))
            elif role == "user":
                messages.append(HumanMessage(content=content))
        messages.append(HumanMessage(content=question))

        response = self.client.invoke(messages)

        token_usage = TokenUsage()
        if hasattr(response, "response_metadata"):
            usage = response.response_metadata.get("token_usage", {})
            token_usage.prompt_tokens = usage.get("prompt_tokens")
            token_usage.completion_tokens = usage.get("completion_tokens")
            token_usage.total_tokens = usage.get("total_tokens")

        return response.content, token_usage

    def chat_stream(self, question: str, context: str, history: list[dict]) -> Iterable[tuple[str, Optional[TokenUsage]]]:
        """
        Stream the response from the model and return chunks along with token information.

        Args:
            question: User's question
            context: Database context (can be empty if has_database_context is False)
            history: Chat history
            has_database_context: Whether the context contains database data

        Yields:
            tuple[str, Optional[TokenUsage]]: Response chunk and optionally token information
        """
        messages = [SystemMessage(content=self._build_system_prompt(context))]
        for item in history:
            role = item.get("role")
            content = item.get("content", "")
            if not content:
                continue
            if role == "assistant":
                messages.append(AIMessage(content=content))
            elif role == "user":
                messages.append(HumanMessage(content=content))
        messages.append(HumanMessage(content=question))

        streaming_client = ChatOpenAI(
            api_key=self.settings.api_key,
            model=self.settings.model,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            streaming=True,
        )

        last_chunk = None
        for chunk in streaming_client.stream(messages):
            last_chunk = chunk
            content = getattr(chunk, "content", "")
            if content:
                yield content, None

        token_usage = None
        if last_chunk and hasattr(last_chunk, "response_metadata"):
            usage = last_chunk.response_metadata.get("token_usage", {})
            if usage:
                token_usage = TokenUsage(
                    prompt_tokens=usage.get("prompt_tokens"),
                    completion_tokens=usage.get("completion_tokens"),
                    total_tokens=usage.get("total_tokens"),
                )

        if token_usage:
            yield "", token_usage

    def _build_system_prompt(self, context: str) -> str:
        base_prompt = "You are an AI assistant for Django Admin.\n\n"
        return (
            base_prompt
            + "INSTRUCTIONS:\n"
            "1. If database context is provided, use it and do not invent data.\n"
            "2. If no database context is provided, answer from general knowledge.\n"
            "3. Keep the response concise and helpful.\n"
            "4. Respond in the same language as the user's question.\n\n"
            f"DATABASE CONTEXT:\n{context or 'No database context provided.'}"
        )
