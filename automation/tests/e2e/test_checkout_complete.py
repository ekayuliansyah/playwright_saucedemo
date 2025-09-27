import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.testdata import DEFAULT_VALID  # <-- perbaikan import

@pytest.mark.smoke
def test_checkout_complete(page, base_url_ui):
    # 1) login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    # 2) inventory
    inv = InventoryPage(page)
    inv.assert_loaded()
    added = inv.add_first_n_items(2)
    inv.open_cart()

    # 3) cart
    cart = CartPage(page)
    cart.assert_loaded()
    cart.expect_badge_equals(2)
    cart_names = cart.listed_item_names()
    assert set(added).issubset(set(cart_names))

    cart.checkout()

    # 4) checkout step one
    checkout = CheckoutPage(page)
    checkout.step_one("John", "Doe", "12345")

    # 5) overview assertions
    checkout.expect_overview()
    prices = checkout.get_overview_prices()
    checkout.assert_summary_math(sum(prices))

    # 6) finish
    checkout.finish()
