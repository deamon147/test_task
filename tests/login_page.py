from playwright.sync_api import Page
from utils.logger import logger

class IFrameHandler:
    def __init__(self, page: Page, selector: str, button_name: str):
        self.iframe = page.frame_locator(selector)
        self.accept_button = self.iframe.get_by_role("button", name=button_name)
    def accept(self):
        if self.accept_button.is_visible():
            try:
                self.accept_button.click()
                logger.info(f"Clicked on '{self.accept_button}' button")
            except Exception as e:
                logger.error(f"Error clicking on '{self.accept_button}': {str(e)}")
        else:
            logger.warning(f"Button '{self.accept_button}' is not visible, skipping")
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        logger.info("Initializing LoginPage")
        self.cookies_iframe = IFrameHandler(page, "iframe[title='SP Consent Message']", "Accept")
        self.ad_iframe = IFrameHandler(page, "iframe[title='Iframe title']", "Accept and continue")
        self.user_avatar = page.locator("div.user_avatar:nth-child(3)")
        self.sign_in_button = page.locator('div.user_avatar a.login[href="/connect/msnt/"][rel="nofollow"]')
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("input[type='submit']")
        self.continue_button = page.locator("#continue_with_this_account")
        self.error_message = page.locator("[class='cmp-tray-alert-title']")
        self.email_error = page.locator("#email-error")
        self.password_error = page.locator("#password-error")
    def navigate(self, url):
        logger.info(f"Navigating to {url}")
        self.page.goto(url)
        self.accept_cookies()
        self.accept_advertisement()
        self.go_to_login_page()

    def accept_cookies(self):
        self.cookies_iframe.accept()

    def accept_advertisement(self):
        self.ad_iframe.accept()
    def go_to_login_page(self):
        self.user_avatar.click()
        self.sign_in_button.click()

    def login(self, email, password):
        logger.info(f"Attempting login with email: {email}")
        self.clear_fields()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        logger.debug("Login credentials submitted")
    def approve_profile(self):
        self.continue_button.click()

    def is_error_popup_visible(self):
        return self.error_message.inner_text()

    def get_email_error_text(self):
        return self.email_error.inner_text() if self.email_error.is_visible() else ""

    def get_password_error_text(self):
        return self.password_error.inner_text() if self.password_error.is_visible() else ""

    def clear_fields(self):
        self.email_input.fill("")
        self.password_input.fill("")
