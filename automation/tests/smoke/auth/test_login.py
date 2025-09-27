from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.testdata import DEFAULT_VALID, NEGATIVE_LOCKED, NEGATIVE_WRONGPASS

@pytest.mark.smoke
def test_login_success_saves_state(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)
    inv = InventoryPage(page)
    inv.assert_loaded()

def test_login_failure_locked_user(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(NEGATIVE_LOCKED.username, NEGATIVE_LOCKED.password)
    login.assert_error("Sorry, this user has been locked out.")

def test_login_failure_wrong_password(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(NEGATIVE_WRONGPASS.username, NEGATIVE_WRONGPASS.password)
    login.assert_error("Username and password do not match")
