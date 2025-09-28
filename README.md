Playwright Saucedemo Automation

This repository contains an end-to-end (E2E), regression, smoke, and negative test suite for SauceDemo
, implemented using Python, Pytest, and Playwright.
The project is designed with clean architecture, reusable components, and CI/CD integration via GitHub Actions.

🚀 Features

Playwright + Pytest for cross-browser automation (Chromium, Firefox, WebKit).

Page Object Model (POM) with reusable components.

Test categories:

Smoke – sanity checks for critical flows.

Regression – full coverage on UI elements and navigation.

E2E – full checkout and login flows.

Negative – edge cases, error handling, and invalid inputs.

Configurable via .env:

Browser type (chromium, firefox, webkit)

Headless mode

Tracing & video recording

Artifacts collection: traces, videos, screenshots for debugging.

GitHub Actions CI/CD with:

Multi-browser test matrix

HTML report upload

Playwright artifacts upload

🛠️ Tech Stack

Language: Python 3.12

Framework: Playwright (sync API)

Testing: Pytest

Reports: Pytest-HTML, Allure

Linting/Formatting: Ruff, Black

Environment Management: Python-dotenv

📂 Project Structure
automation/
│── config/           # Settings & environment variables
│── fixtures/         # Pytest fixtures (browser, context, page)
│── pages/            # Page Object Model classes
│── tests/            # Test suites: smoke, regression, e2e, negative
│── utils/            # Helpers and utilities
artifacts/            # Traces, screenshots, videos (ignored in git)
reports/              # Test reports (ignored in git)
pytest.ini            # Pytest configuration
requirements.txt      # Python dependencies
.github/workflows/    # CI/CD workflows (GitHub Actions)

⚙️ Setup & Installation
1. Clone Repository
git clone https://github.com/ekayuliansyah/playwright_saucedemo.git
cd playwright_saucedemo

2. Create Virtual Environment
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

3. Install Dependencies
pip install -r automation/requirements.txt

4. Install Playwright Browsers
python -m playwright install --with-deps

▶️ Running Tests

Run all tests:

pytest


Run smoke tests only:

pytest -m smoke


Run excluding API tests (as configured in CI):

pytest -m "not api" --html=report.html --self-contained-html

📊 CI/CD with GitHub Actions

The project runs tests automatically on every push and pull request using GitHub Actions.

Workflow file: .github/workflows/tests.yml

Matrix execution: Chromium, Firefox, WebKit

Artifacts uploaded:

HTML report (pytest-report-<browser>)

Traces, videos, and screenshots

Example Workflow Excerpt
strategy:
  fail-fast: false
  matrix:
    browser: [chromium, firefox, webkit]

runs-on: ubuntu-latest

steps:
  - name: Checkout
    uses: actions/checkout@v4
  - name: Setup Python
    uses: actions/setup-python@v5
    with:
      python-version: "3.12"
  - name: Install deps
    run: pip install -r automation/requirements.txt
  - name: Install Playwright
    run: python -m playwright install --with-deps ${{ matrix.browser }}
  - name: Run tests
    run: pytest -m "not api" --html=report.html --self-contained-html

🧾 Example Test Case (Reset App State)
@pytest.mark.negative
def test_reset_app_state_clears_cart(page, base_url_ui):
    login = LoginPage(page)
    login.open(base_url_ui)
    login.login(DEFAULT_VALID.username, DEFAULT_VALID.password)

    inv = InventoryPage(page)
    inv.add_first_n_items(2)
    inv.open_cart()

    cart = CartPage(page)
    cart.expect_badge_equals(2)

    header = HeaderComponent(page)
    header.reset_app_state()
    cart.expect_badge_equals(0)

📌 Notes

.gitignore excludes artifacts, reports, and environment files.

Tests are deterministic; however, network instability from saucedemo.com may occasionally cause retries.

The project can be extended with:

API tests (via httpx)

Visual regression testing

Parallel execution scaling with Pytest-xdist

👤 Author

Ekayuliansyah
