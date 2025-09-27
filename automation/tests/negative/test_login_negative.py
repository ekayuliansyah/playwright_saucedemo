from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from utils.testdata import UserCreds

WRONG = UserCreds("standard_user", "wrong_password")
LOCKED = UserCreds("locked_out_user", "secret_sauce")

@pytest.mark.negative
def test_login_wrong_password_shows_error(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    # Pastikan field & tombol siap
    login.username.wait_for(state="visible")
    login.password.wait_for(state="visible")
    login.login_btn.wait_for(state="visible")

    login.login(WRONG.username, WRONG.password)
    login.assert_error("Epic sadface: Username and password do not match any user in this service")

@pytest.mark.negative
def test_locked_out_user_shows_locked_message(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(LOCKED.username, LOCKED.password)
    login.assert_error("Epic sadface: Sorry, this user has been locked out.")
