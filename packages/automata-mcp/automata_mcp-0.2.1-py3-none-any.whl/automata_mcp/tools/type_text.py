# src/tools/type_text.py
from typing import Any
from automata_mcp.state.state import state

async def type_text_impl(locator_id: str, text: str) -> dict[str, Any]:
    """
    Types text into an input field or textarea.
    Pass the 'locator_id' from get_actionable_elements and the text to type.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "type_text",
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
        # Clear existing value first
        await state.page.fill(locator_id, "")
        await state.page.type(locator_id, text)

        # Optional verification (useful for LLM confidence)
        entered_value = await state.page.locator(locator_id).input_value()

        return {
            "ok": True,
            "action": "type_text",
            "target": locator_id,
            "data": {
                "text_length": len(text),
                "verified": entered_value == text,
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
            "action": "type_text",
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
