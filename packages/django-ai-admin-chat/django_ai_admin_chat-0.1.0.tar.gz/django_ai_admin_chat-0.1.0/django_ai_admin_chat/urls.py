"""
URL configuration for django_ai_admin_chat app.

This file is ready for future implementation of URL patterns for chat functionality.
"""

from django.urls import path

from . import views

app_name = "django_ai_admin_chat"

urlpatterns = [
    path("admin-chat/echo/", views.admin_chat_echo, name="admin-chat-echo"),
    path("admin-chat/history/", views.admin_chat_history, name="admin-chat-history"),
    path("admin-chat/stream/", views.admin_chat_stream, name="admin-chat-stream"),
    path("admin-chat/clear/", views.admin_chat_clear, name="admin-chat-clear"),
]
