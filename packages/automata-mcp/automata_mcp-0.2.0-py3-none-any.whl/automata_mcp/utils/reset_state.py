from state.state import state

async def reset_browser_state():

    try:
        if state.page:
            await state.page.close()
    except Exception:
        pass

    try:
        if state.context:
            await state.context.close()
    except Exception:
        pass

    try:
        if state.browser:
            await state.browser.close()
    except Exception:
        pass

    try:
        if state.playwright:
            await state.playwright.stop()
    except Exception:
        pass

    state.page = None
    state.context = None
    state.browser = None
    state.playwright = None
