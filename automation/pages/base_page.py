from __future__ import annotations
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def expect_title_contains(self, text: str):
        expect(self.page).to_have_title(lambda t: text in t)
