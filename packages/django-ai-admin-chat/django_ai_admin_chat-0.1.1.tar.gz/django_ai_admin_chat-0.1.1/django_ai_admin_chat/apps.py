import logging

from django.apps import AppConfig

from .conf import get_chat_settings

logger = logging.getLogger(__name__)


class DjangoAiAdminChatConfig(AppConfig):
    """Configuration for django_ai_admin_chat app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_ai_admin_chat"
    verbose_name = "Django AI Admin Chat"

    def ready(self) -> None:
        settings = get_chat_settings()
        if settings.provider != "openai":
            logger.warning(
                "Unsupported provider configured for admin chat: %s",
                settings.provider,
            )
        if settings.provider == "openai" and not settings.api_key:
            logger.warning(
                "DJANGO_AI_ADMIN_CHAT_API_KEY is missing. " "Admin chat responses will fail until it is set."
            )
