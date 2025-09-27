# REPLACE WHOLE FILE
from __future__ import annotations
import re
from typing import List
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator(".title")
        # primary & fallback locator untuk dropdown sort
        self._sort_sel_primary = "[data-test='product_sort_container']"
        self._sort_sel_fallback = "select.product_sort_container"
        self.sort_select = page.locator(self._sort_sel_primary)

        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.item_cards = page.locator(".inventory_item")
        self.inventory_list = page.locator(".inventory_list")
        self.add_buttons = page.get_by_role("button", name="Add to cart")

    # ------------ helpers internal ------------
    def _resolve_sort_select(self):
        """
        Pastikan self.sort_select menunjuk ke elemen yang benar.
        Beberapa tema/versi bisa beda attribute; siapkan fallback by class.
        """
        if self.sort_select.count() == 0 or not self.sort_select.is_visible():
            alt = self.page.locator(self._sort_sel_fallback)
            if alt.count() > 0:
                self.sort_select = alt

    # ------------ assertions halaman ------------
    def assert_loaded(self):
        # URL sudah di /inventory.html
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"), timeout=15000)
        # Judul "Products"
        expect(self.title).to_have_text("Products", timeout=10000)
        # Daftar produk muncul dan minimal ada 1 item
        expect(self.inventory_list).to_be_visible(timeout=10000)
        expect(self.item_cards.first).to_be_visible(timeout=10000)

        # Dropdown sort tampil (dengan fallback jika perlu)
        self._resolve_sort_select()
        expect(self.sort_select).to_be_visible(timeout=10000)

    def assert_item_visible(self, name: str):
        """Pastikan item tertentu muncul di inventory."""
        item = self.page.locator(".inventory_item").filter(has_text=name)
        expect(item).to_be_visible(timeout=5000)

    def expect_cart_badge_hidden(self):
        """Pastikan badge tidak muncul (cart kosong)."""
        expect(self.cart_badge).not_to_be_visible()

    # ------------ aksi ------------
    def add_first_n_items(self, n: int = 2) -> List[str]:
        """
        Klik N item pertama, return nama item yang ditambahkan.
        Klik tombol DI DALAM card masing-masing agar urutan nama ↔ tombol tidak mismatch.
        Assert: tombol berubah jadi 'Remove' & badge naik.
        """
        names: List[str] = []
        total_cards = self.item_cards.count()
        count = min(n, total_cards)

        for i in range(count):
            card = self.item_cards.nth(i)
            name = card.locator(".inventory_item_name").inner_text()
            # klik tombol dalam card ini
            btn = card.get_by_role("button", name="Add to cart")
            btn.click()

            # verifikasi tombol berubah menjadi "Remove" pada card yg sama
            expect(card.get_by_role("button", name="Remove")).to_be_visible(timeout=10000)

            names.append(name)

            # verifikasi badge naik; beri timeout lebih longgar
            expect(self.cart_badge).to_have_text(str(i + 1), timeout=10000)

        return names

    def remove_item_by_name(self, name: str):
        """Klik tombol Remove berdasarkan nama item di inventory."""
        card = self.page.locator(".inventory_item").filter(has_text=name)
        btn = card.get_by_role("button", name="Remove")
        expect(btn).to_be_visible(timeout=5000)
        btn.click()
        # Pastikan tombol balik jadi "Add to cart"
        expect(card.get_by_role("button", name="Add to cart")).to_be_visible(timeout=5000)

    def open_item_detail(self, name: str):
        """Klik nama item untuk masuk ke halaman detail produk."""
        card = self.page.locator(".inventory_item").filter(has_text=name)
        link = card.locator(".inventory_item_name")
        expect(link).to_be_visible()
        link.click()

    def open_cart(self):
        self.cart_link.click()

    # ------------ getters ------------
    def get_inventory_item_names(self) -> List[str]:
        return [
            self.item_cards.nth(i).locator(".inventory_item_name").inner_text()
            for i in range(self.item_cards.count())
        ]

    def get_inventory_item_prices(self) -> List[float]:
        prices: List[float] = []
        for i in range(self.item_cards.count()):
            t = self.item_cards.nth(i).locator(".inventory_item_price").inner_text()  # e.g. "$29.99"
            prices.append(float(t.replace("$", "")))
        return prices

    # ------------ sorting ------------
    def sort_by(self, visible_text: str):
        """Pilih opsi sorting berdasarkan label; tunggu visible & verifikasi value berubah."""
        self._resolve_sort_select()
        expect(self.sort_select).to_be_visible(timeout=10000)
        self.sort_select.select_option(label=visible_text)
        expect(self.sort_select).to_have_value(self._map_label_to_value(visible_text))

    # ----- Sorting assertions -----
    def assert_sorted_name_asc(self):
        names = self.get_inventory_item_names()
        assert names == sorted(names), f"Not sorted A→Z: {names}"

    def assert_sorted_name_desc(self):
        names = self.get_inventory_item_names()
        assert names == sorted(names, reverse=True), f"Not sorted Z→A: {names}"

    def assert_sorted_price_low_high(self):
        prices = self.get_inventory_item_prices()
        assert prices == sorted(prices), f"Not sorted low→high: {prices}"

    def assert_sorted_price_high_low(self):
        prices = self.get_inventory_item_prices()
        assert prices == sorted(prices, reverse=True), f"Not sorted high→low: {prices}"

    # ----- helpers -----
    def _map_label_to_value(self, label: str) -> str:
        mapping = {
            "Name (A to Z)": "az",
            "Name (Z to A)": "za",
            "Price (low to high)": "lohi",
            "Price (high to low)": "hilo",
        }
        if label not in mapping:
            raise ValueError(f"Unknown sort label: {label}")
        return mapping[label]
