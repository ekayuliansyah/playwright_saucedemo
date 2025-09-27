from __future__ import annotations

import os
import pytest

# Optional: allure bisa tidak ada di environment tertentu
try:
    import allure  # type: ignore
except Exception:  # pragma: no cover
    allure = None  # fallback agar hook tidak error jika allure tidak terpasang

from config.settings import settings

# Re-export fixtures dari fixtures/browser_fixtures.py
from fixtures.browser_fixtures import (  # noqa: F401
    playwright_instance as _playwright_instance,
    browser as _browser,
    context as _context,
    page as _page,
)

# ---- Re-export fixtures agar bisa dipakai langsung di tests ----
playwright_instance = _playwright_instance
browser = _browser
context = _context
page = _page


@pytest.fixture(scope="session")
def base_url_ui() -> str:
    """Base URL untuk UI (Sauce Demo)."""
    return settings.base_url_ui


@pytest.fixture(scope="session")
def base_url_api() -> str:
    """Base URL untuk API (Reqres)."""
    return settings.base_url_api


# ---------------------------
# Pytest config & reporting
# ---------------------------

def pytest_configure(config: pytest.Config) -> None:
    """
    Daftarkan custom markers agar tidak muncul PytestUnknownMarkWarning
    walau pytest.ini tidak berada di root project.
    """
    config.addinivalue_line("markers", "smoke: critical path checks")
    config.addinivalue_line("markers", "regression: broader coverage")
    config.addinivalue_line("markers", "api: API-only tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Saat test gagal, otomatis ambil screenshot (kalau fixture `page` ada)
    dan attach ke Allure report. File juga disimpan ke artifacts/screenshots/.
    """
    outcome = yield
    report: pytest.TestReport = outcome.get_result()

    # Hanya pada fase 'call' atau 'setup' yang gagal
    if report.failed and report.when in ("call", "setup"):
        pg = item.funcargs.get("page")  # Playwright Page fixture jika ada
        if pg:
            try:
                os.makedirs("artifacts/screenshots", exist_ok=True)
                file_path = os.path.join("artifacts", "screenshots", f"{item.name}.png")
                pg.screenshot(path=file_path, full_page=True)
                if allure:
                    allure.attach.file(
                        file_path,
                        name=f"screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG,  # type: ignore[attr-defined]
                    )
            except Exception:
                # Jangan sampai hook bikin run error hanya karena gagal ambil screenshot
                pass
