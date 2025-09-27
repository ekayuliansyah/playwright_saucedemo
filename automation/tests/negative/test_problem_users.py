# NEW FILE
from __future__ import annotations
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.testdata import UserCreds

PROBLEM = UserCreds("problem_user", "secret_sauce")

@pytest.mark.regression
def test_problem_user_images_ok(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(PROBLEM.username, PROBLEM.password)
    inv = InventoryPage(page)
    inv.assert_loaded()

    # Cek semua img src tidak kosong dan HTTP 200
    imgs = page.locator(".inventory_item img.inventory_item_img")
    count = imgs.count()
    assert count > 0
    for i in range(count):
        src = imgs.nth(i).get_attribute("src")
        assert src and src.strip(), "Image src empty"
        resp = page.request.get(src)
        assert resp.status == 200, f"Image not 200: {src} => {resp.status}"
