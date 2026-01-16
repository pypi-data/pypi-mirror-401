# src/tools/refresh_page.py
from typing import Any
from state.state import state

async def refresh_page_impl() -> dict[str, Any]:
    """Refreshes the current page."""

    if not state.page:
        return {
            "ok": False,
            "action": "refresh_page",
            "target": None,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session.",
                "retryable": False,
            },
        }

    try:
        await state.page.reload(wait_until="domcontentloaded")

        return {
            "ok": True,
            "action": "refresh_page",
            "target": None,
            "data": {
                "reloaded": True
            },
            "page": {
                "url": state.page.url,
                "title": await state.page.title()
            },
            "error": None
        }

    except Exception as e:
        return {
            "ok": False,
            "action": "refresh_page",
            "target": None,
            "data": None,
            "page": {
                "url": state.page.url if state.page else None,
                "title": await state.page.title() if state.page else None
            },
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "retryable": True
            }
        }
