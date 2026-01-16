# src/tools/click_element.py
from typing import Any
from automata_mcp.state.state import state

async def click_element_impl(locator_id: str) -> dict[str, Any]:
    """
    Clicks an element on the current page.
    Pass the 'locator_id' obtained from the get_actionable_elements tool.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "click_element",
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
        # Capture pre-click state
        previous_url = state.page.url
        previous_title = await state.page.title()

        await state.page.click(locator_id, timeout=10_000)

        # Capture post-click state
        current_url = state.page.url
        current_title = await state.page.title()

        navigated = (
            previous_url != current_url
            or previous_title != current_title
        )

        return {
            "ok": True,
            "action": "click_element",
            "target": locator_id,
            "data": {
                "navigated": navigated,
            },
            "page": {
                "url": current_url,
                "title": current_title,
            },
            "error": None,
        }

    except Exception as e:
        return {
            "ok": False,
            "action": "click_element",
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
