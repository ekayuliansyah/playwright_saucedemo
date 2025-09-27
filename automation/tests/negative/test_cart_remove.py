from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.testdata import DEFAULT_VALID

@pytest.mark.negative
def test_remove_item_in_cart_updates_badge(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # add 2 item → badge 2
    inv.add_first_n_items(2)
    inv.open_cart()

    cart = CartPage(page)
    cart.assert_loaded()
    cart.expect_badge_equals(2)

    # remove 1 item → badge 1
    cart.remove_first_item()
    cart.expect_badge_equals(1)

    # lanjut belanja (opsional), balik ke inventory
    cart.continue_shopping()
    inv.assert_loaded()
