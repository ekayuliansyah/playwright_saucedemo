# REPLACE WHOLE FILE
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.testdata import DEFAULT_VALID


@pytest.mark.negative
def test_checkout_step_one_requires_fields(page, base_url_ui):
    # login & add 1 item
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()
    inv.add_first_n_items(1)
    inv.open_cart()

    cart = CartPage(page)
    cart.assert_loaded()
    cart.checkout()

    checkout = CheckoutPage(page)
    checkout.expect_step_one()

    # 1) Semua field kosong → error First Name
    checkout.continue_without_data()
    checkout.expect_error_message("Error: First Name is required")

    # 2) Isi First Name saja → error Last Name
    checkout.first.fill("John")
    checkout.continue_btn.click()
    checkout.expect_error_message("Error: Last Name is required")

    # 3) Isi First + Last → error Postal Code
    checkout.last.fill("Doe")
    checkout.continue_btn.click()
    checkout.expect_error_message("Error: Postal Code is required")

    # 4) Isi semua field → lanjut ke overview
    checkout.postal.fill("12345")
    checkout.continue_btn.click()
    checkout.expect_overview()
