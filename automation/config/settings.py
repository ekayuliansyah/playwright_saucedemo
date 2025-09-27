from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# load .env file kalau ada
load_dotenv()

@dataclass(frozen=True)
class Settings:
    base_url_ui: str = os.getenv("BASE_URL_UI", "https://www.saucedemo.com/")
    base_url_api: str = os.getenv("BASE_URL_API", "https://reqres.in/")
    browser: str = os.getenv("BROWSER", "chromium")  # chromium|firefox|webkit
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    trace: str = os.getenv("TRACE", "retain-on-failure")  # on|off|retain-on-failure
    video: str = os.getenv("VIDEO", "retain-on-failure")  # off|on|retain-on-failure
    username: str = os.getenv("USERNAME", "standard_user")
    password: str = os.getenv("PASSWORD", "secret_sauce")

settings = Settings()
