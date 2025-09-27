from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    PATH = "/"  # root of saucedemo

    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_btn = page.get_by_role("button", name="Login")
        self.error_msg = page.locator("[data-test=error]")

    def open(self, base_url: str):
        self.page.goto(base_url)
        expect(self.login_btn).to_be_visible()

    def login(self, user: str, pwd: str):
        self.username.fill("")
        self.username.fill(user)
        self.password.fill("")
        self.password.fill(pwd)
        self.login_btn.click()

    def assert_error(self, contains: str):
        expect(self.error_msg).to_contain_text(contains)
