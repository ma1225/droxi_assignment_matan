from playwright.sync_api import Page, Locator
import logging

logger = logging.getLogger(__name__)

class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.trello_username_field: Locator = page.locator('#username-uid1')
        self.trello_password_field: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("a:has-text('Log In')")
        self.continue_button: Locator = page.locator("#login-submit")
        self.board_link = page.get_by_text("Droxi")

    def navigate_to_trello(self, trello_url: str):
        self.page.goto(trello_url)

    def login_to_trello(self, username: str, password: str):
        self.login_button.click()
        self.trello_username_field.fill(username)
        self.continue_button.click()
        self.trello_password_field.fill(password)
        self.login_button.click()
        self.board_link.click()
