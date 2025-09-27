from __future__ import annotations
import pathlib
import pytest
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page
from config.settings import settings

ARTIFACTS_DIR = pathlib.Path("artifacts")
STATE_DIR = ARTIFACTS_DIR / ".auth"
STATE_FILE = STATE_DIR / "ui_state.json"


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Global Playwright instance untuk seluruh sesi tes."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """
    Browser instance (Chromium/Firefox/WebKit) sesuai env.
    Contoh di .env:
      BROWSER=chrome | chromium | firefox | webkit
    """
    browser_name = settings.browser.lower()

    if browser_name == "chrome":
        browser = playwright_instance.chromium.launch(
            channel="chrome", headless=settings.headless
        )
    elif browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=settings.headless)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=settings.headless)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=settings.headless)
    else:
        raise ValueError(
            f"Unsupported browser: {browser_name}. "
            "Gunakan salah satu dari: chrome | chromium | firefox | webkit"
        )

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Context baru per test dengan trace & video sesuai setting."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        record_video_dir=str(ARTIFACTS_DIR / "videos") if settings.video != "off" else None,
        storage_state=str(STATE_FILE) if STATE_FILE.exists() else None,
        base_url=settings.base_url_ui,
    )

    if settings.trace in {"on", "retain-on-failure"}:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    # Simpan trace di akhir test
    if settings.trace != "off":
        (ARTIFACTS_DIR / "traces").mkdir(parents=True, exist_ok=True)
        ctx.tracing.stop(path=str(ARTIFACTS_DIR / "traces" / "trace.zip"))
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Page baru per test."""
    return context.new_page()
