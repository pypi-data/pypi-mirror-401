"""
Django admin configuration for django_ai_admin_chat app.

This file is ready for future implementation of admin chat functionality.
"""

from django.contrib import admin

from .models import ChatHistory


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for ChatHistory model."""

    list_display = [
        "id",
        "session_id",
        "user",
        "query_preview",
        "search_type",
        "tokens_total",
        "created_at",
    ]
    list_filter = ["search_type", "created_at", "user", "session_id"]
    search_fields = ["query", "response", "session_id"]
    readonly_fields = [
        "session_id",
        "user",
        "query",
        "search_type",
        "search_results",
        "context",
        "response",
        "tokens_prompt",
        "tokens_completion",
        "tokens_total",
        "chat_history",
        "created_at",
    ]
    date_hierarchy = "created_at"

    def query_preview(self, obj):
        """Return a shortened version of the query."""
        if len(obj.query) > 50:
            return obj.query[:50] + "..."
        return obj.query

    query_preview.short_description = "Query"

    def has_add_permission(self, request):
        """Disable manual addition of history."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing of history."""
        return False


