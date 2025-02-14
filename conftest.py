import pytest
from playwright.sync_api import sync_playwright
from utils.logger import logger

@pytest.fixture(scope="function")
def page():
    logger.info("Initializing browser context")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        yield page
        logger.info("Closing browser context")
        browser.close()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        setattr(report, "duration_formatted", f"{report.duration:.2f}s")