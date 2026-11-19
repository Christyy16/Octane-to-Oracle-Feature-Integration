from playwright.sync_api import sync_playwright
from config import SWAGGER_URL
import requests


def get_session():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(SWAGGER_URL)

        input("Login complete? Press Enter")

        cookies = page.context.cookies()

        browser.close()
    
    session = requests.Session()

    for cookie in cookies:

        session.cookies.set(
            cookie["name"],
            cookie["value"]
        )
    
    return session