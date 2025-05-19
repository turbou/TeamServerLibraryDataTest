import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://contrast.nginx/Contrast/static/ng/index.html#/pages/signin")
    page.get_by_test_id("username-email").click()
    page.get_by_test_id("username-email").fill("contrast_superadmin@contrastsecurity.com")
    page.get_by_test_id("password").click()
    page.get_by_test_id("password").fill("default1!")
    page.get_by_test_id("log-in-button").click()
    time.sleep(3)
    page.goto("http://contrast.nginx/Contrast/static/ng/admin_index.html#/superadmin/settings/general")
    page.locator("ng-form").filter(has_text="Proxy Connect your internet").locator("i").nth(1).click()
    page.get_by_role("button", name="Save", exact=True).click()
    page.get_by_role("button", name="Update").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
