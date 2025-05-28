#!/usr/bin/env python3

# import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()


def save_calendar(page, group_id, file_name):
    """
    Takes page object and group id from schoology and saves ics
    """
    print(f"https://app.schoology.com/group/{group_id}")
    page.goto(f"https://app.schoology.com/group/{group_id}", timeout=0)
    #time.sleep(10)
    page.get_by_role("button", name="Calendar").click()
    print('here')
    page.get_by_role("link", name="Export").click()
    url = f"https://app.schoology.com/calendar/feed/export/group/{group_id}/download"
    # with page.expect_download() as download_info:
    #    page.get_by_role("link", name="Download Calendar").click()
    # download = download_info.value
    # download.save_as(file_name)
    # return download

    url = f"https://app.schoology.com/calendar/feed/export/group/{group_id}/download"
    with page.expect_download() as download_info:
        page.goto(url)
        download = download_info.value
        download.save_as(file_name)
        return download


def run(playwright: Playwright) -> None:
    pw = os.getenv("AG_PW")
    user = os.getenv("AG_USER")
    save_dir = os.getenv("AG_SAVE_DIR")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    page.goto("https://app.schoology.com/login")
    page.get_by_placeholder("Email or Username").click()
    page.get_by_placeholder("Email or Username").fill(user)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(pw)
    page.get_by_role("button", name="Log in").click()
    page.get_by_role("button", name="Elie Michael-Ruddy Elie").click()
    page.get_by_role("menuitem", name="Robert Ruddy Robert Ruddy").click()
    page.wait_for_url("https://app.schoology.com/parent/home")

    save_calendar(page, "542092501", f"{save_dir}/hs-band.ics")
    # save_calendar(page, "542095419", f"{save_dir}/hs-percussion.ics")
    save_calendar(page, "516620983", f"{save_dir}/hs-girls-xc.ics")
    save_calendar(page, "517074687", f"{save_dir}/hs-swimming.ics")
    save_calendar(page, "6230763180", f"{save_dir}/ms-xc.ics")
    save_calendar(page, "517158427", f"{save_dir}/hs-track.ics")
    save_calendar(page, "733432165", f"{save_dir}/hs-theater.ics")

    # page.get_by_role("link", name="Close").nth(1).click()
    # page.get_by_role("link", name="Close").click()
    # page.get_by_role("button", name="Robert Ruddy Robert Ruddy").click()
    # page.get_by_role("menuitem", name="Logout").click()

    # ---------------------
    page.goto("https://app.schoology.com/logout")
    context.close()
    browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
