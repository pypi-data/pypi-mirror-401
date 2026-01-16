# src/tools/select_option.py
from typing import Any
from state.state import state

async def select_option_impl(locator_id: str, option_value: str) -> dict[str, Any]:
    """Selects an option from a dropdown."""

    if not state.page:
        return {
            "ok": False,
            "action": "select_option",
            "target": locator_id,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session. Call 'open_browser' first.",
                "retryable": False,
            },
        }

    try:
        await state.page.locator(locator_id).select_option(option_value)

        return {
            "ok": True,
            "action": "select_option",
            "target": locator_id,
            "data": {
                "selected_value": option_value
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
            "action": "select_option",
            "target": locator_id,
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
