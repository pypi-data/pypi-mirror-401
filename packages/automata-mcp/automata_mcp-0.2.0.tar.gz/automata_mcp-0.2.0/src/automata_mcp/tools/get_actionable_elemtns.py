# src/tools/get_actionable_elements.py
from typing import Any
import json
from state.state import state
from utils.actionable_elements import get_actionable_elements_for_llm

async def get_actionable_elements_impl() -> dict[str, Any]:
    """
    Returns a structured list of actionable elements for the LLM.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "get_actionable_elements",
            "target": None,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session. Call 'open_browser' first.",
                "retryable": False,
            },
        }

    try:
        elements_json = await get_actionable_elements_for_llm(state.page)
        elements = json.loads(elements_json)

        return {
            "ok": True,
            "action": "get_actionable_elements",
            "target": None,
            "data": {
                "count": len(elements),
                "elements": elements,
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
            "action": "get_actionable_elements",
            "target": None,
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
