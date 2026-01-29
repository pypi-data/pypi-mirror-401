"""
Views for django_ai_admin_chat app.
"""

import json
import logging
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .conf import get_chat_settings
from .langchain_service import LangChainChatService, TokenUsage
from .models import ChatHistory
from .search import SearchMatch, SQLDatabaseChainSearchService

logger = logging.getLogger(__name__)


def _get_or_create_session_id(request):
    """Get or create session_id for the current chat session."""
    if "admin_chat_session_id" not in request.session:
        request.session["admin_chat_session_id"] = str(uuid.uuid4())
        request.session.modified = True
    return request.session["admin_chat_session_id"]


def _search_matches_to_json(matches: list[SearchMatch]) -> list[dict]:
    """Convert a list of SearchMatch to JSON."""
    return [{"model_label": match.model_label, "display": match.display} for match in matches]


def _save_chat_history(
    request,
    query: str,
    search_type: str,
    matches: list[SearchMatch],
    context: str,
    response: str,
    token_usage: TokenUsage | None,
    chat_history: list[dict],
    session_id: str,
    sql_query: str | None = None,
    raw_sql_results: list[dict] | None = None,
):
    """Save chat history to the database."""
    try:
        ChatHistory.objects.create(
            session_id=session_id,
            user=request.user if request.user.is_authenticated else None,
            query=query,
            search_type=search_type,
            search_results=_search_matches_to_json(matches),
            context=context,
            response=response,
            tokens_prompt=token_usage.prompt_tokens if token_usage else None,
            tokens_completion=token_usage.completion_tokens if token_usage else None,
            tokens_total=token_usage.total_tokens if token_usage else None,
            chat_history=chat_history,
            sql_query=sql_query,
            raw_sql_results=raw_sql_results,
        )
    except Exception as exc:
        logger.exception("Error saving chat history: %s", exc)


@staff_member_required
@require_POST
def admin_chat_echo(request):
    """Chat endpoint that returns a chat history list."""
    message = (request.POST.get("message") or "").strip()
    messages = request.session.get("admin_chat_messages", [])
    session_id = _get_or_create_session_id(request)

    if message:
        search_type = None
        matches = []
        context = ""
        token_usage = None
        search_service = None
        sql_query = None
        raw_sql_results = None
        try:
            settings = get_chat_settings()
            chat_service = LangChainChatService(settings=settings)

            search_service = SQLDatabaseChainSearchService(
                settings=settings, max_results=settings.max_search_results
            )
            search_type = ChatHistory.SEARCH_TYPE_SQL_DATABASE_CHAIN
            matches = search_service.search(message, chat_history=messages)
            context = search_service.build_context(matches)
            if search_type == ChatHistory.SEARCH_TYPE_SQL_DATABASE_CHAIN and isinstance(
                search_service, SQLDatabaseChainSearchService
            ):
                try:
                    sql_query = search_service.get_latest_sql_query()
                    raw_sql_results = search_service.get_raw_sql_results()
                    logger.debug("SQL query extracted: %s", sql_query)
                    logger.debug("Raw SQL results extracted: %s", raw_sql_results)
                except Exception:
                    pass

            response_text, token_usage = chat_service.chat(question=message, context=context, history=messages)
        except Exception as exc:
            logger.exception("Admin chat error: %s", exc)
            response_text = "An error occurred while processing the query. " "Please try again."
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response_text})
        request.session["admin_chat_messages"] = messages

        _save_chat_history(
            request=request,
            query=message,
            search_type=search_type or ChatHistory.SEARCH_TYPE_NONE,
            matches=matches,
            context=context,
            response=response_text,
            token_usage=token_usage,
            chat_history=messages[:-2],
            session_id=session_id,
            sql_query=sql_query,
            raw_sql_results=raw_sql_results,
        )
    return JsonResponse({"messages": messages})


@staff_member_required
@require_GET
def admin_chat_history(request):
    """Return chat history for the current admin session."""
    messages = request.session.get("admin_chat_messages", [])
    return JsonResponse({"messages": messages})


@staff_member_required
@require_http_methods(["GET", "POST"])
def admin_chat_stream(request):
    """Stream chat response via Server-Sent Events."""
    if request.method == "POST":
        message = (request.POST.get("message") or "").strip()
    else:
        message = (request.GET.get("message") or "").strip()
    messages = request.session.get("admin_chat_messages", [])
    session_id = _get_or_create_session_id(request)

    if not message:
        return JsonResponse({"messages": messages}, status=400)

    messages.append({"role": "user", "content": message})
    request.session["admin_chat_messages"] = messages
    request.session.modified = True
    request.session.save()

    def event_stream():
        response_parts: list[str] = []
        search_type = None
        matches = []
        context = ""
        token_usage = None
        search_service = None
        sql_query = None
        raw_sql_results = None
        try:
            settings = get_chat_settings()
            chat_service = LangChainChatService(settings=settings)

            search_service = SQLDatabaseChainSearchService(
                settings=settings, max_results=settings.max_search_results
            )
            search_type = ChatHistory.SEARCH_TYPE_SQL_DATABASE_CHAIN
            # Pass chat history excluding the current message that was just added
            chat_history_for_search = messages[:-1] if messages else []
            matches = search_service.search(message, chat_history=chat_history_for_search)
            context = search_service.build_context(matches)
            for chunk, chunk_token_usage in chat_service.chat_stream(
                question=message, context=context, history=messages
            ):
                if chunk_token_usage:
                    token_usage = chunk_token_usage
                if chunk:
                    response_parts.append(chunk)
                    payload = json.dumps({"chunk": chunk})
                    yield f"data: {payload}\n\n"
        except Exception as exc:
            logger.exception("Admin chat streaming error: %s", exc)
            error_message = "An error occurred while processing the query. " "Please try again."
            response_parts = [error_message]
            payload = json.dumps({"error": error_message})
            yield f"data: {payload}\n\n"
        finally:
            response_text = "".join(response_parts)
            if response_text:
                messages.append({"role": "assistant", "content": response_text})
                request.session["admin_chat_messages"] = messages
                request.session.modified = True
                request.session.save()

                sql_query = None
                raw_sql_results = None
                if (
                    search_type == ChatHistory.SEARCH_TYPE_SQL_DATABASE_CHAIN
                    and search_service
                ):
                    try:
                        if isinstance(search_service, SQLDatabaseChainSearchService):
                            sql_query = search_service.get_latest_sql_query()
                            raw_sql_results = search_service.get_raw_sql_results()
                            logger.debug("SQL query extracted: %s", sql_query)
                            logger.debug("Raw SQL results extracted: %s", raw_sql_results)
                    except Exception:
                        pass

                _save_chat_history(
                    request=request,
                    query=message,
                    search_type=search_type or ChatHistory.SEARCH_TYPE_NONE,
                    matches=matches,
                    context=context,
                    response=response_text,
                    token_usage=token_usage,
                    chat_history=messages[:-2],
                    session_id=session_id,
                    sql_query=sql_query,
                    raw_sql_results=raw_sql_results,
                )
            yield 'data: {"done": true}\n\n'

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response


@staff_member_required
@require_POST
def admin_chat_clear(request):
    """Clear chat history for the current admin session and start a new session."""
    old_session_id = request.session.get("admin_chat_session_id")

    request.session["admin_chat_messages"] = []

    new_session_id = str(uuid.uuid4())
    request.session["admin_chat_session_id"] = new_session_id
    request.session.modified = True
    request.session.save()

    logger.info("Chat session cleared: old_session_id=%s, new_session_id=%s", old_session_id, new_session_id)
    print(f"\n[CHAT CLEAR] New session created: {new_session_id} (previous: {old_session_id})\n")

    return JsonResponse({"messages": []})
