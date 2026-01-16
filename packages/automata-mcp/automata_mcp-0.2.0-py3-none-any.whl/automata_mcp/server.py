from typing import Any, Optional
import asyncio
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import json
import os 
import sys
import subprocess
from utils.install_playwright import install_playwright

from tools.open_browser import open_browser_impl
from tools.navigate_to import navigate_to_impl
from tools.finish import finish_impl
from tools.get_actionable_elemtns import get_actionable_elements_impl
from tools.click_element import click_element_impl
from tools.type_text import type_text_impl
from tools.extract_text_from_page import extract_text_from_page_impl
from tools.get_element_text import get_element_text_impl
from tools.get_element_attribute import get_element_attribute_impl
from tools.select_option import select_option_impl
from tools.get_page_url import get_page_url_impl
from tools.go_back import go_back_impl
from tools.go_forward import go_forward_impl
from tools.refresh_page import refresh_page_impl
from tools.hover_element import hover_element_impl
from tools.scroll_page import scroll_page_impl
from tools.double_click import double_click_element_impl
from tools.right_click_element import right_click_element_impl
from tools.check_page_contains_text import check_page_contains_text_impl
# Initialize FastMCP server
mcp = FastMCP("automata-playwright-mcp")


@mcp.tool()
async def open_browser(url: str, headless: bool = True) -> dict[str, Any]:
    """
    Opens a browser and navigates to a URL.
    Defaults to headless mode (no UI) unless headless=False is passed.
    If a browser is already open, it reuses it but navigates to the new URL.
    """
    return await open_browser_impl(url, headless)
    

@mcp.tool()
async def navigate_to(url: str) -> dict:
    """
    Navigates the currently open browser to a new URL.
    Use this when the browser is already open and you want to change the address.
    """

    return await navigate_to_impl(url)
    


@mcp.tool()
async def finish() -> dict:
    """
    Safely closes the active browser and cleans up resources.
    """
    return await finish_impl()

    
@mcp.tool()
async def get_actionable_elements() -> dict:
    """Returns a structured list of actionable elements for the LLM."""
    return await get_actionable_elements_impl()


@mcp.tool()
async def click_element(locator_id: str) -> dict:
    """
    Clicks an element on the current page.
    Pass the 'locator_id' obtained from the get_actionable_elements tool.
    """

    return await click_element_impl(locator_id)


@mcp.tool()
async def type_text(locator_id: str, text: str) -> dict:
    """
    Types text into an input field or textarea.
    Pass the 'locator_id' from get_actionable_elements and the text to type.
    """
    return await type_text_impl(locator_id, text)
    


@mcp.tool()
async def extract_text_from_page() -> dict:
    """
    Extracts all visible text from the page.
    Use this to find prices, product names, or verify order totals.
    """

    return await extract_text_from_page_impl()

    
@mcp.tool()
async def get_element_text(locator_id: str) -> dict:
    """
    Extracts text from a specific element.
    Use this to accurately get a product's price or name once you have its locator.
    """

    return await get_element_text_impl(locator_id)


@mcp.tool()
async def get_element_attribute(locator_id: str, attribute: str) -> dict:
    """Gets a specific attribute value from an element."""
    return await get_element_attribute_impl(locator_id, attribute)
    
    
@mcp.tool()
async def select_option(locator_id: str, option_value: str) -> dict:
    """Selects an option from a dropdown."""

    return await select_option_impl(locator_id, option_value)
    
@mcp.tool()
async def get_page_url() -> dict:
    """Returns the current page URL."""

    return await get_page_url_impl()


@mcp.tool()
async def go_back() -> dict:
    """Goes back to the previous page."""

    return await go_back_impl()


@mcp.tool()
async def go_forward() -> dict:
    """Goes forward to the next page."""

    return await go_forward_impl()


@mcp.tool()
async def refresh_page() -> dict:
    """Refreshes the current page."""

    return await refresh_page_impl()

    
@mcp.tool()
async def hover_element(locator_id: str) -> dict:
    """Hovers over an element to trigger hover states."""

    return await hover_element_impl(locator_id)

    

@mcp.tool()
async def scroll_page(direction: str, pixels: int = 500) -> dict:
    """Scrolls the page in a direction (up/down/left/right)."""

    return await scroll_page_impl(direction, pixels)


@mcp.tool()
async def double_click_element(locator_id: str) -> dict:
    """Double-clicks an element."""
    return await double_click_element_impl(locator_id)
    


@mcp.tool()
async def right_click_element(locator_id: str) -> dict:
    """Right-clicks an element."""

    return await right_click_element_impl(locator_id)

    


@mcp.tool()
async def check_page_contains_text(text: str) -> dict:
    """Checks if visible page text contains a specific string."""

    return await check_page_contains_text_impl(text)

    


def main():
    """Main entry point for the MCP server."""

    first_run_file = os.path.expanduser(
        "~/.automata_playwright_mcp_installed"
    )

    if not os.path.exists(first_run_file):
        print("First run detected. Installing Playwright browsers...")
        if install_playwright():
            os.makedirs(os.path.dirname(first_run_file), exist_ok=True)
            with open(first_run_file, "w") as f:
                f.write("installed")

    mcp.run()


if __name__ == "__main__":
    main()