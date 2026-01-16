# src/tools/extract_text_from_page.py
from typing import Any
from state.state import state

MAX_CHARS = 15_000

async def extract_text_from_page_impl() -> dict[str, Any]:
    """
    Extracts all visible text from the page.
    Useful for prices, product names, or order verification.
    """

    if not state.page:
        return {
            "ok": False,
            "action": "extract_text_from_page",
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
        text = await state.page.evaluate(
            """
            () => {
                const nodes = document.querySelectorAll('script, style, nav, footer');
                nodes.forEach(n => n.remove());

                return document.body.innerText
                    .replace(/\\n\\s*\\n/g, '\\n')
                    .trim();
            }
            """
        )

        truncated = len(text) > MAX_CHARS

        return {
            "ok": True,
            "action": "extract_text_from_page",
            "target": None,
            "data": {
                "text": text[:MAX_CHARS],
                "truncated": truncated,
                "char_count": min(len(text), MAX_CHARS),
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
            "action": "extract_text_from_page",
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
