#!/usr/bin/env python3

import re, os, requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv


load_dotenv()

def playwright_login_get_cookies():

    pw = os.getenv("AG_PW")
    user = os.getenv("AG_USER")

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

def requests_download_with_cookies(cookies, group_id, file_name):
    session = requests.Session()
    download_url=f'https://app.schoology.com/calendar/feed/export/group/{group_id}/download'

    # Convert Playwright cookies to Requests cookies
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    # Perform the download
    resp = session.get(download_url)
    with open(file_name, "wb") as f:
        f.write(resp.content)
    print(f"Download complete for {file_name}")


save_dir = os.getenv("AG_SAVE_DIR")
os.makedirs(save_dir, exist_ok=True)
group_list = (
            ('516620983', f'{save_dir}/hs-girls-xc.ics'),
            ('542092501', f'{save_dir}/hs-band.ics'),
            ('542095419', f'{save_dir}/hs-percussion.ics'),
            ('517074687', f'{save_dir}/hs-swimming.ics'),
            ('6230763180', f'{save_dir}/ms-xc.ics'),
            ('517158427', f'{save_dir}/hs-track.ics'),
            ('733432165', f'{save_dir}/hs-theater.ics'),
        )

cookies = playwright_login_get_cookies()
print('Received credentials')
for group_id, file_name in group_list:
    requests_download_with_cookies(cookies, group_id, file_name)
