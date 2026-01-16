# src/tools/go_forward.py
from typing import Any
from state.state import state

async def go_forward_impl() -> dict[str, Any]:
    """Goes forward to the next page."""

    if not state.page:
        return {
            "ok": False,
            "action": "go_forward",
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
        response = await state.page.go_forward(timeout=10000)

        return {
            "ok": True,
            "action": "go_forward",
            "target": None,
            "data": {
                "navigated": response is not None
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
            "action": "go_forward",
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
