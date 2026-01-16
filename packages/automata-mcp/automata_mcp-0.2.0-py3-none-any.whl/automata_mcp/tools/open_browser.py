# tools/browser_impl.py
from typing import Any
from playwright.async_api import async_playwright
from state.state import state
from utils.reset_state import reset_browser_state

async def open_browser_impl(url: str, headless: bool = True) -> dict[str, Any]:
    try:
        if state.browser or state.playwright:
            await reset_browser_state()

        state.playwright = await async_playwright().start()
        state.browser = await state.playwright.chromium.launch(headless=headless)
        state.context = await state.browser.new_context()
        state.page = await state.context.new_page()

        # Navigate to URL
        response = await state.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        if not response:
            return {
                "ok": False,
                "action": "open_browser",
                "target": url,
                "data": None,
                "page": None,
                "error": {
                    "type": "NoResponse",
                    "message": "No response received from server",
                    "retryable": True,
                },
            }

        return {
            "ok": True,
            "action": "open_browser",
            "target": url,
            "data": {
                "status": response.status,
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
            "action": "open_browser",
            "target": url,
            "data": None,
            "page": {
                "url": state.page.url if state.page else None,
                "title": await state.page.title() if state.page else None,
            },
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "retryable": False,
            },
        }
