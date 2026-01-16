# src/tools/hover_element.py
from typing import Any
from automata_mcp.state.state import state

async def hover_element_impl(locator_id: str) -> dict[str, Any]:
    """Hovers over an element to trigger hover states."""

    if not state.page:
        return {
            "ok": False,
            "action": "hover_element",
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
        await state.page.locator(locator_id).hover()

        return {
            "ok": True,
            "action": "hover_element",
            "target": locator_id,
            "data": {
                "hovered": True
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
            "action": "hover_element",
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
