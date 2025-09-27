# REPLACE WHOLE FILE
from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.testdata import DEFAULT_VALID, DEFAULT_PERSON

@pytest.mark.parametrize("viewport", [(1440, 900), (390, 844)])
def test_add_to_cart_and_checkout_overview(page, base_url_ui, viewport):
    # 1) viewport
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})

    # 2) login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    # 3) inventory loaded
    inv = InventoryPage(page)
    inv.assert_loaded()

    # 4) add 2 items, assert badge naik setiap klik
    added_names = inv.add_first_n_items(2)
    assert len(added_names) == 2

    # 5) open cart
    inv.open_cart()

    # 6) cart loaded + verifikasi nama & badge
    cart = CartPage(page)
    cart.assert_loaded()
    cart.expect_badge_equals(2)
    cart_names = cart.listed_item_names()
    assert set(added_names).issubset(set(cart_names)), f"Cart items mismatch: {cart_names} vs {added_names}"

    # 7) ambil harga dari cart untuk dasar perhitungan di overview
    cart_prices = cart.listed_item_prices()
    expected_subtotal = round(sum(cart_prices), 2)

    # 8) checkout step 1 (isi data)
    cart.checkout()
    checkout = CheckoutPage(page)
    checkout.step_one(DEFAULT_PERSON.first, DEFAULT_PERSON.last, DEFAULT_PERSON.postal)

    # 9) overview tampil + verifikasi math subtotal & total
    checkout.expect_overview()
    checkout.assert_summary_math(expected_subtotal)

    # 10) jangan submit pembayaran (sesuai scope) – test selesai
