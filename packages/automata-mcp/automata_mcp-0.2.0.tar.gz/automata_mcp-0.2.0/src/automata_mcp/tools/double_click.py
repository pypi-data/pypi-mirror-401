# src/tools/double_click_element.py
from typing import Any
from state.state import state

async def double_click_element_impl(locator_id: str) -> dict[str, Any]:
    """Double-clicks an element."""

    if not state.page:
        return {
            "ok": False,
            "action": "double_click_element",
            "target": locator_id,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session.",
                "retryable": False,
            },
        }

    try:
        await state.page.locator(locator_id).dblclick()

        return {
            "ok": True,
            "action": "double_click_element",
            "target": locator_id,
            "data": {
                "double_clicked": True
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
            "action": "double_click_element",
            "target": locator_id,
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
