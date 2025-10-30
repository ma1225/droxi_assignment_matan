import pytest
from typing import Generator, Any
from playwright.sync_api import Page, Playwright, sync_playwright, Browser

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Generator[Browser, Any, None]:
    """Create a shared browser instance for all tests"""
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create an isolated context for each test"""
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context) -> Generator[Page, Any, None]:
    """Create a new page for each test"""
    page = context.new_page()
    yield page
    page.close()
