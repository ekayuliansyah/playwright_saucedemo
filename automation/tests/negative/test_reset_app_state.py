import pytest
from utils.testdata import DEFAULT_VALID
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.components.header_component import HeaderComponent


@pytest.mark.negative
def test_reset_app_state_clears_cart(page, base_url_ui):
    # 1) login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # 2) tambah 2 item
    inv.add_first_n_items(2)
    inv.open_cart()

    cart = CartPage(page)
    cart.assert_loaded()
    cart.expect_badge_equals(2)

    # 3) reset app state dari menu
    header = HeaderComponent(page)
    header.reset_app_state()

    # 4) cek badge hilang
    assert cart.cart_badge.count() == 0, "Badge masih ada padahal harus hilang setelah reset"

    # 5) cek item di cart kosong
    cart_items = cart.listed_item_names()
    assert cart_items == [] or len(cart_items) == 0, f"Cart masih ada item: {cart_items}"
