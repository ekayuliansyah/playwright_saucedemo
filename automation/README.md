# Automation: Sauce Demo (UI) + Reqres (API)


## Prasyarat
- Python 3.11+
- Node tidak wajib, tapi Playwright butuh `playwright install --with-deps`


## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps