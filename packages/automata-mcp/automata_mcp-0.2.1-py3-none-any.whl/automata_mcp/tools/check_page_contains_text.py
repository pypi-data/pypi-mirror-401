# src/tools/check_page_contains_text.py
from typing import Any

from automata_mcp.state.state import state

async def check_page_contains_text_impl(text: str) -> dict[str, Any]:
    """Checks if visible page text contains a specific string."""

    if not state.page:
        return {
            "ok": False,
            "action": "check_page_contains_text",
            "target": text,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session.",
                "retryable": False,
            },
        }

    try:
        visible_text = await state.page.evaluate(
            "() => document.body.innerText"
        )

        found = text in visible_text

        return {
            "ok": True,
            "action": "check_page_contains_text",
            "target": text,
            "data": {
                "found": found
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
            "action": "check_page_contains_text",
            "target": text,
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
