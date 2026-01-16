# src/tools/get_element_attribute.py
from typing import Any
from automata_mcp.state.state import state

async def get_element_attribute_impl(locator_id: str, attribute: str) -> dict[str, Any]:
    """
    Gets a specific attribute value from an element.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "get_element_attribute",
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
        value = await state.page.locator(locator_id).get_attribute(attribute)

        return {
            "ok": True,
            "action": "get_element_attribute",
            "target": locator_id,
            "data": {
                "attribute": attribute,
                "value": value,
                "is_present": value is not None,
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
            "action": "get_element_attribute",
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
