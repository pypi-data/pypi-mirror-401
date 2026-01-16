import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import requests

class Browser:
    def __init__(self, url=None, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.response = None
        if url:
            self.goto(url)

    def goto(self, url: str):
        self.driver.get(url)

    def get_html(self):
        return self.driver.page_source

    def get_title(self):
        return self.driver.title

    def click(self, selector: str):
        el = self.driver.find_element(By.CSS_SELECTOR, selector)
        el.click()

    def type(self, selector: str, text: str):
        el = self.driver.find_element(By.CSS_SELECTOR, selector)
        el.clear()
        el.send_keys(text)

    def get_info(self):
        url = self.driver.current_url
        parsed = urlparse(url)
        if not self.response:
            try:
                self.response = requests.get(url, timeout=10)
            except Exception:
                self.response = None
        return {
            "url": url,
            "scheme": parsed.scheme,
            "domain": parsed.netloc.split(":")[0],
            "subdomain": ".".join(parsed.netloc.split(".")[:-2]) if len(parsed.netloc.split(".")) > 2 else "",
            "path": parsed.path,
            "status_code": self.response.status_code if self.response else None,
            "title": self.get_title()
        }

    def is_online(self):
        if not self.response:
            try:
                self.response = requests.head(self.driver.current_url, timeout=5)
            except Exception:
                return False
        return self.response.status_code < 400 if self.response else False

    def get_html_content(self):
        if not self.response:
            try:
                self.response = requests.get(self.driver.current_url, timeout=10)
            except Exception:
                return None
        return self.response.text if self.response else None

    def send_request(self, method="GET", data=None, headers=None):
        try:
            self.response = requests.request(method.upper(), self.driver.current_url, data=data, headers=headers, timeout=10)
            return {
                "status_code": self.response.status_code,
                "headers": dict(self.response.headers),
                "text": self.response.text
            }
        except Exception as e:
            return {"error": str(e)}

    def quit(self):
        self.driver.quit()
