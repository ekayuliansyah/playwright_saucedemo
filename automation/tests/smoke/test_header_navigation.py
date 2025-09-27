import pytest
from utils.testdata import DEFAULT_VALID
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.components.header_component import HeaderComponent


@pytest.mark.smoke
def test_go_to_all_items_from_cart(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    # buka cart dulu
    inv.open_cart()
    header = HeaderComponent(page)

    # klik All Items → kembali ke inventory
    header.go_to_all_items()
    inv.assert_loaded()


@pytest.mark.smoke
def test_go_to_about_redirects(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    header = HeaderComponent(page)
    header.go_to_about()

    # verifikasi diarahkan ke halaman eksternal Sauce Labs (cek URL domain)
    expect_url = page.url
    assert "saucelabs.com" in expect_url, f"Unexpected about page URL: {expect_url}"
