# src/tools/get_page_url.py
from typing import Any
from state.state import state

async def get_page_url_impl() -> dict[str, Any]:
    """Returns the current page URL."""

    if not state.page:
        return {
            "ok": False,
            "action": "get_page_url",
            "target": None,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session.",
                "retryable": False,
            },
        }

    return {
        "ok": True,
        "action": "get_page_url",
        "target": None,
        "data": {
            "url": state.page.url
        },
        "page": {
            "url": state.page.url,
            "title": await state.page.title(),
        },
        "error": None,
    }
