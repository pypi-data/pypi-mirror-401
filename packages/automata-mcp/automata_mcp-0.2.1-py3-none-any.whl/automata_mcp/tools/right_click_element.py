# src/tools/right_click_element.py
from typing import Any
from automata_mcp.state.state import state

async def right_click_element_impl(locator_id: str) -> dict[str, Any]:
    """Right-clicks an element."""

    if not state.page:
        return {
            "ok": False,
            "action": "right_click_element",
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
        await state.page.locator(locator_id).click(button="right")

        return {
            "ok": True,
            "action": "right_click_element",
            "target": locator_id,
            "data": {
                "right_clicked": True
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
            "action": "right_click_element",
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
