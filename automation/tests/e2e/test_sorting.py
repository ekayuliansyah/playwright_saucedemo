# NEW FILE
from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.testdata import DEFAULT_VALID

@pytest.mark.regression
def test_sorting_all_options(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # A → Z
    inv.sort_by("Name (A to Z)")
    inv.assert_sorted_name_asc()

    # Z → A
    inv.sort_by("Name (Z to A)")
    inv.assert_sorted_name_desc()

    # Price low → high
    inv.sort_by("Price (low to high)")
    inv.assert_sorted_price_low_high()

    # Price high → low
    inv.sort_by("Price (high to low)")
    inv.assert_sorted_price_high_low()
