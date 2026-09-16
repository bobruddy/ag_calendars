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


def is_ics(content):
    start = content.lstrip(b"\xef\xbb\xbf \t\r\n")
    return start.startswith(b"BEGIN:VCALENDAR")


def requests_download_with_cookies(cookies, group_id, file_path):
    session = requests.Session()
    download_url = f"https://app.schoology.com/calendar/feed/export/group/{group_id}/download"

    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])

    resp = session.get(download_url)
    if not is_ics(resp.content):
        print(
            f"Skipping {file_path.name}: not an ICS calendar "
            f"(group {group_id}, status {resp.status_code})"
        )
        if file_path.exists() and not is_ics(file_path.read_bytes()):
            file_path.unlink()
            print(f"Removed invalid existing file {file_path.name}")
        return False

    file_path.write_bytes(resp.content)
    print(f"Download complete for {file_path.name}")
    return True


def main():
    save_dir = Path(os.getenv("AG_SAVE_DIR"))
    save_dir.mkdir(parents=True, exist_ok=True)

    with open(SCRIPT_DIR / "calendars.json") as f:
        calendars = json.load(f)

    cookies = playwright_login_get_cookies()
    print("Received credentials")

    failed = []
    for cal in calendars:
        dest = save_dir / cal["file"]
        if not requests_download_with_cookies(cookies, cal["group"], dest):
            failed.append(cal["file"])

    if failed:
        print("Failed downloads: " + ", ".join(failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
