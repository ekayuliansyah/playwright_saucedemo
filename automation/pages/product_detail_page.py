# REPLACE WHOLE FILE
from __future__ import annotations
import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    PATH_PATTERN = re.compile(r"/inventory-item\.html\?id=\d+")

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator(".inventory_details_name")
        self.desc = page.locator(".inventory_details_desc")
        self.price = page.locator(".inventory_details_price")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.back_btn = page.get_by_role("button", name="Back to products")
        self.add_btn = page.get_by_role("button", name="Add to cart")
        self.remove_btn = page.get_by_role("button", name="Remove")

    # ---------- Assertions ----------
    def assert_loaded(self):
        expect(self.page).to_have_url(self.PATH_PATTERN, timeout=10000)
        expect(self.title).to_be_visible()
        expect(self.desc).to_be_visible()
        expect(self.price).to_be_visible()

    def assert_product_matches(self, expected_name: str):
        expect(self.title).to_have_text(expected_name)

    # ---------- Actions ----------
    def add_to_cart(self):
        self.add_btn.click()
        expect(self.remove_btn).to_be_visible(timeout=5000)
        expect(self.cart_badge).to_have_text("1", timeout=5000)

    def remove_from_cart(self):
        self.remove_btn.click()
        expect(self.add_btn).to_be_visible(timeout=5000)
        # badge bisa hilang jika kosong
        if self.cart_badge.count() > 0:
            expect(self.cart_badge).to_have_text("0")

    def open_cart(self):
        self.cart_link.click()

    def back_to_inventory(self):
        self.back_btn.click()
