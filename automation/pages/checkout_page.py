# REPLACE WHOLE FILE
from __future__ import annotations
from typing import Tuple, List
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Step One fields
        self.first = page.get_by_placeholder("First Name")
        self.last = page.get_by_placeholder("Last Name")
        self.postal = page.get_by_placeholder("Zip/Postal Code")
        self.continue_btn = page.get_by_role("button", name="Continue")
        self.cancel_btn = page.get_by_role("button", name="Cancel")
        self.title_div = page.locator(".title")
        self.error_msg = page.locator("[data-test='error']")

        # Step Two (Overview)
        self.finish_btn = page.get_by_role("button", name="Finish")
        self.summary_subtotal = page.locator(".summary_subtotal_label")
        self.summary_tax = page.locator(".summary_tax_label")
        self.summary_total = page.locator(".summary_total_label")
        self.overview_items = page.locator(".cart_item")

    # ---------- Step One ----------
    def expect_step_one(self):
        """Pastikan halaman Step One (Your Information) muncul."""
        expect(self.title_div).to_have_text("Checkout: Your Information")
        expect(self.first).to_be_visible()
        expect(self.last).to_be_visible()
        expect(self.postal).to_be_visible()

    def step_one(self, first: str, last: str, postal: str):
        self.first.fill(first)
        self.last.fill(last)
        self.postal.fill(postal)
        self.continue_btn.click()

    def continue_without_data(self):
        """Klik Continue tanpa isi field apapun."""
        self.continue_btn.click()

    def expect_error_message(self, expected: str):
        """Pastikan pesan error sesuai harapan."""
        expect(self.error_msg).to_have_text(expected)

    # ---------- Step Two (Overview) ----------
    def expect_overview(self):
        expect(self.title_div).to_have_text("Checkout: Overview")

    def get_overview_prices(self) -> List[float]:
        return [
            float(
                self.overview_items.nth(i).locator(".inventory_item_price").inner_text().replace("$", "")
            )
            for i in range(self.overview_items.count())
        ]

    def parse_money(self, text: str) -> float:
        return float(text.split("$")[-1].strip())

    def read_summary(self) -> Tuple[float, float, float]:
        subtotal = self.parse_money(self.summary_subtotal.inner_text())
        tax = self.parse_money(self.summary_tax.inner_text())
        total = self.parse_money(self.summary_total.inner_text())
        return subtotal, tax, total

    def assert_summary_math(self, expected_subtotal: float):
        subtotal, tax, total = self.read_summary()
        assert round(subtotal, 2) == round(expected_subtotal, 2), \
            f"Subtotal mismatch: {subtotal} != {expected_subtotal}"
        assert round(subtotal + tax, 2) == round(total, 2), \
            f"Total mismatch: subtotal({subtotal}) + tax({tax}) != total({total})"

    # ---------- Actions ----------
    def cancel(self):
        self.cancel_btn.click()

    def finish(self):
        self.finish_btn.click()
