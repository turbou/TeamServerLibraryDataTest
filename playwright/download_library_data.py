import re
import os
import sys
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    env_not_found = False
    for env_key in ['CONTRAST_HUB_USERNAME', 'CONTRAST_HUB_PASSWORD', 'LIB_DATA_DATE']:
        if not env_key in os.environ:
            print('Environment variable %s is not set' % env_key)
            env_not_found |= True
    if env_not_found:
        sys.exit(1)

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://hub.contrastsecurity.com/h/index.html")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill(os.environ['CONTRAST_HUB_USERNAME'])
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(os.environ['CONTRAST_HUB_PASSWORD'])
    page.get_by_role("button", name="Log in").click()

    page.goto("https://hub.contrastsecurity.com/h/download/all/typed.html", timeout=180000)
    page.get_by_role("link", name="Library Data Exports").click(timeout=180000)
    with page.expect_download(timeout=180000) as download_md5_info:
        page.get_by_role("row", name="%s Contrast-Data-" % os.environ['LIB_DATA_DATE']).get_by_role("link", name="MD5 Sum").first.click()
    download_md5 = download_md5_info.value
    #file_md5_path = download_md5.path()
    #print(file_md5_path)
    download_md5.save_as('/app/' + download_md5.suggested_filename)

    with page.expect_download(timeout=1800000) as download_zip_info:
        page.get_by_role("row", name="%s Contrast-Data-" % os.environ['LIB_DATA_DATE']).get_by_role("button").click()
    download_zip = download_zip_info.value
    #file_zip_path = download_zip.path()
    #print(file_zip_path)
    download_zip.save_as('/app/' + download_zip.suggested_filename)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

