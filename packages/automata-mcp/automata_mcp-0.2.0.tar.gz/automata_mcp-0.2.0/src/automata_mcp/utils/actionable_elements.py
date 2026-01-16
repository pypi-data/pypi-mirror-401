# src/utils/actionable_elements.py
import json
from playwright.async_api import Page

async def get_actionable_elements_for_llm(page: Page) -> str:
    """
    Extracts structured, token-efficient JSON data for actionable elements
    using a single page.evaluate() call.
    """

    ACTIONABLE_SELECTOR = 'a, button, input:not([type="hidden"]), textarea, select, [role="button"], [role="link"], [tabindex]'

    # 2. Execute a single JavaScript function in the browser context
    elements_data = await page.evaluate(f"""
        (selector) => {{
            const elements = document.querySelectorAll(selector);
            const data = [];

            elements.forEach((el, index) => {{
                // Check if the element is visually rendered (offsetWidth > 0) to avoid hidden elements
                if (el.offsetWidth > 0 && el.offsetHeight > 0) {{
                    
                    // Generate a Playwright-preferred locator string using accessibility attributes
                    let locator_strategy = '';
                    if (el.id) {{
                        locator_strategy = `#${{el.id}}`;
                    }} else if (el.placeholder) {{
                        locator_strategy = `[placeholder="${{el.placeholder.substring(0, 50)}}"]`;
                    }} else if (el.hasAttribute('aria-label')) {{
                        locator_strategy = `[aria-label="${{el.getAttribute('aria-label').substring(0, 50)}}"]`;
                    }} else if (el.getAttribute('data-testid')) {{
                        locator_strategy = `[data-testid="${{el.getAttribute('data-testid')}}"]`;
                    }} else {{
                        // Fallback to text content and tag name (LESS RELIABLE)
                        const textContent = el.textContent ? el.textContent.trim().substring(0, 50) : '';
                        if (textContent) {{
                            locator_strategy = `text="${{textContent}}"`;
                        }} else {{
                            locator_strategy = el.tagName.toLowerCase();
                        }}
                    }}

                    // Create the clean, structured data object
                    data.push({{
                        "index": index,
                        "tag": el.tagName.toLowerCase(),
                        "role": el.getAttribute('role') || el.tagName.toLowerCase(),
                        "locator_id": locator_strategy, 
                        "text": el.textContent.trim().substring(0, 50),
                        "placeholder": el.placeholder || '',
                        "name": el.name || '',
                        "type": el.type || el.getAttribute('type') || '',
                    }});
                }}
            }});
            return data;
        }}
    """, ACTIONABLE_SELECTOR)

    # Return the structured data as a token-efficient JSON string
    return json.dumps(elements_data, indent=2)
