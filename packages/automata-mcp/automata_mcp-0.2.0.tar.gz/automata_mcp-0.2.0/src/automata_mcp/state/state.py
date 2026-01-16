# state.py
from typing import Optional
from playwright.async_api import Browser, BrowserContext, Page, Playwright

class BrowserState:
    playwright: Optional[Playwright] = None
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None

state = BrowserState()
