import json
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://egaz.uz/user/socialize/egov"
LOGIN = "azizbeksadiqov"
PASSWORD = "Aa934140270$"

def refresh_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(LOGIN_URL)

        page.fill('input[name="login"]', LOGIN)
        page.fill('input[name="password"]', PASSWORD)

        page.click('button[type="submit"]')

        # networkidle emas — bu EGAZda ishlamaydi
        page.wait_for_url("http://egaz.uz/admin", timeout=20000)

        cookies = context.cookies()
        print("Yangi cookie olindi:", cookies)
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=4)

        browser.close()
        return True
