#!/usr/bin/env python3

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

SCRIPT_DIR = Path(__file__).resolve().parent


def playwright_login_get_cookies():
    user = os.getenv("AG_USER")
    pw = os.getenv("AG_PW")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://app.schoology.com/login")
        page.get_by_role("textbox", name="Email or Username (required):").click()
        page.get_by_role("textbox", name="Email or Username (required):").fill(user)
        page.get_by_role("textbox", name="Password (required):").click()
        page.get_by_role("textbox", name="Password (required):").fill(pw)
        page.get_by_role("button", name="Log in").click()

        cookies = context.cookies()
        browser.close()
        return cookies


def requests_download_with_cookies(cookies, group_id, file_path):
    session = requests.Session()
    download_url = f"https://app.schoology.com/calendar/feed/export/group/{group_id}/download"

    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])

    resp = session.get(download_url)
    file_path.write_bytes(resp.content)
    print(f"Download complete for {file_path.name}")


def main():
    save_dir = Path(os.getenv("AG_SAVE_DIR"))
    save_dir.mkdir(parents=True, exist_ok=True)

    with open(SCRIPT_DIR / "calendars.json") as f:
        calendars = json.load(f)

    cookies = playwright_login_get_cookies()
    print("Received credentials")

    for cal in calendars:
        dest = save_dir / cal["file"]
        requests_download_with_cookies(cookies, cal["group"], dest)


if __name__ == "__main__":
    main()
