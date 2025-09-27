# REPLACE WHOLE FILE
from __future__ import annotations
import re
from typing import List
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator(".title")
        self.checkout_btn = page.get_by_role("button", name="Checkout")
        self.continue_shopping_btn = page.get_by_role("button", name="Continue Shopping")
        self.cart_items = page.locator(".cart_item")
        self.cart_badge = page.locator(".shopping_cart_badge")

    # ---- Assertions ----
    def assert_loaded(self):
        expect(self.page).to_have_url(re.compile(r"/cart\.html$"))
        expect(self.title).to_have_text("Your Cart")
        # jika cart berisi item, minimal item pertama terlihat
        if self.cart_items.count() > 0:
            expect(self.cart_items.first).to_be_visible(timeout=5000)

    def expect_badge_equals(self, expected: int):
        expect(self.cart_badge).to_have_text(str(expected))

    def expect_item_count(self, expected: int):
        expect(self.cart_items).to_have_count(expected)

    def assert_cart_empty(self):
        """Pastikan cart kosong (tidak ada item & tidak ada badge)."""
        expect(self.cart_items).to_have_count(0)
        expect(self.cart_badge).not_to_be_visible()

    # ---- Data getters ----
    def listed_item_names(self) -> List[str]:
        return [
            self.cart_items.nth(i).locator(".inventory_item_name").inner_text()
            for i in range(self.cart_items.count())
        ]

    def listed_item_prices(self) -> List[float]:
        prices: List[float] = []
        for i in range(self.cart_items.count()):
            t = self.cart_items.nth(i).locator(".inventory_item_price").inner_text()
            prices.append(float(t.replace("$", "")))
        return prices

    # ---- Actions ----
    def checkout(self):
        self.checkout_btn.click()

    def continue_shopping(self):
        self.continue_shopping_btn.click()

    def remove_first_item(self):
        """Remove item pertama dari cart."""
        if self.cart_items.count() == 0:
            raise AssertionError("Cart kosong, tidak ada item untuk dihapus")
        first_item = self.cart_items.first
        btn = first_item.get_by_role("button", name="Remove")
        expect(btn).to_be_visible()
        btn.click()

    def remove_item_by_name(self, name: str):
        """Remove item berdasarkan nama produk di cart."""
        item = self.cart_items.filter(has_text=name)
        expect(item).to_be_visible()
        btn = item.get_by_role("button", name="Remove")
        expect(btn).to_be_visible()
        btn.click()
