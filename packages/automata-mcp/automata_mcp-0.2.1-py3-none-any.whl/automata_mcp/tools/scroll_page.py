# src/tools/scroll_page.py
from typing import Any
from automata_mcp.state.state import state

async def scroll_page_impl(direction: str, pixels: int = 500) -> dict[str, Any]:
    """Scrolls the page in a direction (up/down/left/right)."""

    if not state.page:
        return {
            "ok": False,
            "action": "scroll_page",
            "target": direction,
            "data": None,
            "page": None,
            "error": {
                "type": "NoSession",
                "message": "No active browser session.",
                "retryable": False,
            },
        }

    try:
        direction = direction.lower()

        if direction == "down":
            await state.page.evaluate("window.scrollBy(0, arguments[0])", pixels)
        elif direction == "up":
            await state.page.evaluate("window.scrollBy(0, arguments[0])", -pixels)
        elif direction == "right":
            await state.page.evaluate("window.scrollBy(arguments[0], 0)", pixels)
        elif direction == "left":
            await state.page.evaluate("window.scrollBy(arguments[0], 0)", -pixels)
        else:
            return {
                "ok": False,
                "action": "scroll_page",
                "target": direction,
                "data": None,
                "page": {
                    "url": state.page.url,
                    "title": await state.page.title(),
                },
                "error": {
                    "type": "InvalidInput",
                    "message": "Direction must be up, down, left, or right.",
                    "retryable": False,
                },
            }

        return {
            "ok": True,
            "action": "scroll_page",
            "target": direction,
            "data": {
                "pixels": pixels,
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
            "action": "scroll_page",
            "target": direction,
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
