import pytest
from playwright.sync_api import Page
from tests.login_page import LoginPage
from utils.config import BASE_URL, VALID_EMAIL, VALID_PASSWORD, INVALID_EMAIL, INVALID_PASSWORD
from utils.logger import logger

@pytest.mark.positive
def test_successful_login(page: Page):
    logger.info("Starting positive login test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    login_page.approve_profile()
    assert "nc=1" in page.url
    logger.info("Positive login test completed")

@pytest.mark.negative
def test_invalid_login(page: Page):
    logger.info("Starting incorrect login data test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    assert login_page.is_error_popup_visible(), "Error popup did not appear"
    logger.info("Incorrect login data test completed")
@pytest.mark.negative
def test_empty_fields(page: Page):
    logger.info("Starting empty fields test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login("", "")
    assert "This field is required!" in login_page.get_email_error_text()
    assert "This field is required!" in login_page.get_password_error_text()
    logger.info("Empty fields test completed")

@pytest.mark.negative
def test_invalid_email_format(page: Page):
    logger.info("Starting invalid email test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login("1", VALID_PASSWORD)
    assert "Please enter a valid email address" in login_page.get_email_error_text()
    logger.info("Invalid email test completed")

@pytest.mark.negative
def test_short_password(page: Page):
    logger.info("Starting short password test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(VALID_EMAIL, "1234")
    assert "Please enter at least 5 characters" in login_page.get_password_error_text()
    logger.info("Short password test completed")

@pytest.mark.negative
def test_long_password(page: Page):
    logger.info("Starting long password test")
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    long_password = "a" * 41
    login_page.login(VALID_EMAIL, long_password)
    assert "Please enter no more than 40 characters" in login_page.get_password_error_text()
    logger.info("Long password test completed")