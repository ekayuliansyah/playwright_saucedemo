from __future__ import annotations
from playwright.sync_api import expect
import pytest

@pytest.mark.smoke
def test_homepage_loads(page, base_url_ui):
    page.goto(base_url_ui)
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    # Playwright Python butuh string/regex, bukan lambda
    expect(page).to_have_title("Swag Labs")
