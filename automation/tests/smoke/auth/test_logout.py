import pytest
from utils.testdata import DEFAULT_VALID
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.components.header_component import HeaderComponent


@pytest.mark.smoke
def test_logout_redirects_to_login(page, base_url_ui):
    # login
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.assert_loaded()

    header = HeaderComponent(page)
    header.logout()

    # cek login page muncul lagi
    expect_login = page.locator("[data-test='username']")
    expect_login.wait_for()
