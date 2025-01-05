import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class WebDriverFactory:
    def __init__(self, browser="chrome", headless=False):
        self.browser = browser
        self.headless = headless

    def get_webdriver(self):
        if self.browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless or os.getenv("GITHUB_ACTIONS"):
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        elif self.browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if self.headless or os.getenv("GITHUB_ACTIONS"):
                options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Браузер {self.browser} не підтримується")

        return driver