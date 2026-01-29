"""Settings helpers for django_ai_admin_chat."""

from dataclasses import dataclass

from django.conf import settings


@dataclass(frozen=True)
class ChatSettings:
    """Resolved settings for the admin chat integration."""

    provider: str
    api_key: str | None
    model: str
    temperature: float
    max_search_results: int
    max_tokens: int
    search_type: str
    allowed_models: list[str]
    excluded_models: list[str]


def _get_setting(name: str, default):
    return getattr(settings, name, default)


def _normalize_search_type(raw_value: str) -> str:
    normalized = (raw_value or "").strip().lower()
    if normalized in {"sql_database_chain"}:
        return normalized
    if normalized in {"sqldatabasechain", "sql_database_chain", "sql-database-chain"}:
        return "sql_database_chain"
    return "sql_database_chain"


def get_chat_settings() -> ChatSettings:
    """Return chat settings resolved from Django settings."""
    return ChatSettings(
        provider=_get_setting("DJANGO_AI_ADMIN_CHAT_PROVIDER", "openai"),
        api_key=_get_setting("DJANGO_AI_ADMIN_CHAT_API_KEY", None),
        model=_get_setting("DJANGO_AI_ADMIN_CHAT_MODEL", "gpt-3.5-turbo"),
        temperature=float(_get_setting("DJANGO_AI_ADMIN_CHAT_TEMPERATURE", 0.7)),
        max_search_results=int(_get_setting("DJANGO_AI_ADMIN_CHAT_MAX_SEARCH_RESULTS", 10)),
        max_tokens=int(_get_setting("DJANGO_AI_ADMIN_CHAT_MAX_TOKENS", 500)),
        search_type=_normalize_search_type(_get_setting("DJANGO_AI_ADMIN_CHAT_SEARCH_TYPE", "sql_database_chain")),
        allowed_models=list(_get_setting("DJANGO_AI_ADMIN_CHAT_ALLOWED_MODELS", [])),
        excluded_models=list(_get_setting("DJANGO_AI_ADMIN_CHAT_EXCLUDED_MODELS", [])),
    )


def is_model_excluded(model_label: str, settings: ChatSettings) -> bool:
    """Check if a model is excluded based on settings.

    Always excludes django_ai_admin_chat.ChatHistory.
    Also excludes any models in excluded_models list.
    """
    if model_label == "django_ai_admin_chat.ChatHistory":
        return True
    return model_label in settings.excluded_models


def is_model_allowed(model_label: str, settings: ChatSettings) -> bool:
    """Check if a model is allowed based on settings.

    A model is allowed if:
    - It's not excluded (always excludes ChatHistory and any in excluded_models)
    - AND either allowed_models is empty (all allowed) or model is in allowed_models

    If allowed_models is empty, all models are allowed (except excluded ones).
    Otherwise, only models in the list are allowed (except excluded ones).
    """
    if is_model_excluded(model_label, settings):
        return False
    if not settings.allowed_models:
        return True
    return model_label in settings.allowed_models
