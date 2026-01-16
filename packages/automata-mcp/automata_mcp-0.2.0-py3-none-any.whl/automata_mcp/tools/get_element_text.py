# src/tools/get_element_text.py
from typing import Any
from state.state import state

async def get_element_text_impl(locator_id: str) -> dict[str, Any]:
    """
    Extracts text from a specific element using its locator.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "get_element_text",
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
        element = state.page.locator(locator_id)

        text = await element.inner_text(timeout=5000)
        text = text.strip()

        return {
            "ok": True,
            "action": "get_element_text",
            "target": locator_id,
            "data": {
                "text": text,
                "char_count": len(text),
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
            "action": "get_element_text",
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
