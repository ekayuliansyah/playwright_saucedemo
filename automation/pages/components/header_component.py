from __future__ import annotations
import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HeaderComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.menu_wrap = page.locator(".bm-menu-wrap")
        self.all_items_link = page.get_by_role("link", name="All Items")
        self.about_link = page.get_by_role("link", name="About")
        self.logout_link = page.get_by_role("link", name="Logout")
        self.reset_link = page.get_by_role("link", name="Reset App State")

    # --- helpers menu ---
    def open_menu(self):
        """Pastikan menu terbuka."""
        # kalau menu masih terbuka, tutup dulu
        if self.menu_wrap.count() > 0 and self.menu_wrap.get_attribute("aria-hidden") == "false":
            self.close_menu()

        self.menu_button.wait_for(state="visible")
        self.menu_button.click()
        expect(self.menu_wrap).to_have_attribute("aria-hidden", "false", timeout=5000)

    def close_menu(self):
        """Tutup menu jika terbuka."""
        if self.menu_wrap.count() > 0 and self.menu_wrap.get_attribute("aria-hidden") == "false":
            try:
                self.menu_button.click(force=True)
            except Exception:
                self.page.keyboard.press("Escape")

            expect(self.menu_wrap).to_have_attribute("aria-hidden", "true", timeout=5000)

    def expect_menu_closed(self):
        """Pastikan menu benar-benar tertutup atau sudah tidak ada lagi."""
        if self.menu_wrap.count() == 0:
            # menu sudah hilang (misalnya setelah logout → ke halaman login)
            return
        expect(self.menu_wrap).to_have_attribute("aria-hidden", "true", timeout=5000)

    # --- actions ---
    def go_to_all_items(self):
        self.open_menu()
        self.all_items_link.click()
        self.expect_menu_closed()
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))

    def go_to_about(self):
        self.open_menu()
        self.about_link.click()
        expect(self.page).to_have_url(re.compile(r"saucelabs\.com"), timeout=15000)

    def logout(self):
        """Klik logout lalu pastikan redirect ke halaman login."""
        self.open_menu()
        self.logout_link.click()
        # jangan maksa tunggu menu wrap, karena DOM bisa hilang
        expect(self.page).to_have_url(re.compile(r"/$"), timeout=5000)

    def reset_app_state(self):
        """Klik Reset App State lalu refresh halaman biar cart kosong."""
        self.open_menu()
        self.reset_link.click()

        # tutup menu pakai tombol / ESC kalau masih terbuka
        if self.menu_wrap.count() > 0 and self.menu_wrap.get_attribute("aria-hidden") == "false":
            try:
                self.menu_button.click(force=True)
            except Exception:
                self.page.keyboard.press("Escape")

        # langsung refresh untuk pastikan state benar-benar reset
        self.page.reload()
