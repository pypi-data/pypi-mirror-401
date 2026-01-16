# src/tools/finish.py
from typing import Any
from automata_mcp.utils.reset_state import reset_browser_state
from automata_mcp.state.state import state

async def finish_impl() -> dict[str, Any]:
    """
    Safely closes the active browser and cleans up Playwright resources.
    """

    try:
        await reset_browser_state()
        return {
            "ok": True,
            "action": "finish",
            "target": None,
            "data": None,
            "page": None,
            "error": None,
        }

    except Exception as e:
        return {
            "ok": False,
            "action": "finish",
            "target": None,
            "data": None,
            "page": None,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "retryable": False,
            },
        }
