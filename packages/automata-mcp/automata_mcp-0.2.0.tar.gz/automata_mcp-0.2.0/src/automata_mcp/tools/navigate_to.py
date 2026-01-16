# src/tools/navigate_to.py
from typing import Any
from state.state import state

async def navigate_to_impl(url: str) -> dict[str, Any]:
    """
    Navigates the currently open browser to a new URL.
    Assumes a browser session is already active.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "navigate_to",
            "target": url,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session found. Call 'open_browser' first.",
                "retryable": False,
            },
        }

    try:
        response = await state.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        if not response:
            return {
                "ok": False,
                "action": "navigate_to",
                "target": url,
                "data": None,
                "page": {
                    "url": state.page.url,
                    "title": await state.page.title(),
                },
                "error": {
                    "type": "NoResponse",
                    "message": "Navigation failed: no response from server",
                    "retryable": True,
                },
            }

        return {
            "ok": True,
            "action": "navigate_to",
            "target": url,
            "data": {
                "status": response.status,
            },
            "page": {
                "url": state.page.url,
                "title": await state.page.title(),
            },
            "error": None,
        }

    except Exception as e:
        return {
            "ok": False,
            "action": "navigate_to",
            "target": url,
            "data": None,
            "page": {
                "url": state.page.url if state.page else None,
                "title": await state.page.title() if state.page else None,
            },
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "retryable": True,
            },
        }
