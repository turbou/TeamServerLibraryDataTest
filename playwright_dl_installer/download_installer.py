import re
import os
import sys 
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    env_not_found = False
    for env_key in ['CONTRAST_HUB_USERNAME', 'CONTRAST_HUB_PASSWORD', 'FILE_NAME']:
        if not env_key in os.environ:
            print('Environment variable %s is not set' % env_key)
            env_not_found |= True
    if env_not_found:
        sys.exit(1)

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://hub.contrastsecurity.com/h/index.html")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(os.environ['CONTRAST_HUB_USERNAME'])
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(os.environ['CONTRAST_HUB_PASSWORD'])
    page.get_by_role("button", name="Log In").click()

    page.goto("https://hub.contrastsecurity.com/h/home.html")
    page.get_by_role("link", name="Linux Installers").click()
    with page.expect_download() as download_md5_info:
        page.get_by_role("row", name=os.environ['FILE_NAME']).get_by_role("link", name="MD5 Sum").first.click()
    download_md5 = download_md5_info.value
    download_md5.save_as('/work/' + download_md5.suggested_filename)

    with page.expect_download() as download_sh_info:
        page.get_by_role("row", name=os.environ['FILE_NAME']).get_by_role("button", name="Download").click()
    download_sh = download_sh_info.value
    download_sh.save_as('/work/' + download_sh.suggested_filename)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

