# Playwright Saucedemo Tests

Automated UI tests for [saucedemo.com](https://www.saucedemo.com) using **Playwright** + **Pytest**.

## 🚀 Features
- End-to-end tests with Playwright
- Page Object Model (POM) structure
- Recordings: videos, screenshots, traces
- Fixtures & reusable components
- Configurable via `.env` file

## 📦 Installation
Clone repository:
```bash
git clone https://github.com/ekayuliansyah/playwright_saucedemo.git
cd playwright_saucedemo


# Automation: Sauce Demo (UI) + Reqres (API)


## Prasyarat
- Python 3.11+
- Node tidak wajib, tapi Playwright butuh `playwright install --with-deps`


## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps