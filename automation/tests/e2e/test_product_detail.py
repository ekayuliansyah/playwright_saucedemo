# REPLACE WHOLE FILE
import pytest
from utils.testdata import DEFAULT_VALID
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage


@pytest.mark.smoke
def test_open_product_detail_and_back(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    # buka inventory
    inv = InventoryPage(page)
    inv.assert_loaded()

    # ambil nama item pertama
    first_name = inv.get_inventory_item_names()[0]

    # klik item → masuk ke detail
    inv.item_cards.nth(0).locator(".inventory_item_name").click()

    detail = ProductDetailPage(page)
    detail.assert_loaded()
    detail.assert_product_matches(first_name)

    # balik ke inventory
    detail.back_to_inventory()
    inv.assert_loaded()


@pytest.mark.smoke
def test_add_and_remove_from_product_detail(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # buka detail item pertama
    inv.item_cards.nth(0).locator(".inventory_item_name").click()

    detail = ProductDetailPage(page)
    detail.assert_loaded()

    # add to cart
    detail.add_to_cart()

    # remove from cart
    detail.remove_from_cart()


@pytest.mark.negative
def test_remove_without_add_shows_add_button(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # buka detail item pertama
    inv.item_cards.nth(0).locator(".inventory_item_name").click()

    detail = ProductDetailPage(page)
    detail.assert_loaded()

    # langsung cek tombol "Add to cart" harus tersedia
    assert detail.add_btn.is_visible(), "Expected 'Add to cart' button to be visible by default"
