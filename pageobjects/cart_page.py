from decimal import Decimal
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


from pageobjects.base_page import BasePage
from helper import extract_decimal_price


@dataclass
class Product:
    name: str
    model: str
    quantity: str
    unit_price: Decimal
    total: Decimal


@dataclass
class SummaryTable:
    name: str
    value: Decimal


class CartPage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=checkout/cart'

    def get_table(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, 'table-responsive')

    def get_rows(self) -> list[WebElement]:
        return self.get_table().find_elements(By.TAG_NAME, 'tr')[1:]

    def get_products(self) -> list[Product]:
        products = []

        for row in self.get_rows():
            cells = row.find_elements(By.TAG_NAME, "td")
            product = Product(
                name=cells[1].text.split("\n")[0].strip(),
                model=cells[2].text.strip(),
                quantity=cells[3].find_element(By.TAG_NAME, "input").get_attribute("value").strip(),
                unit_price=Decimal(extract_decimal_price(cells[4].text.strip())),
                total=Decimal(extract_decimal_price(cells[5].text.strip()))
            )
            products.append(product)
        return products

    def get_summary_table(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, 'col-sm-offset-8')

    def get_summary_rows(self) -> list[WebElement]:
        return self.get_summary_table().find_elements(By.TAG_NAME, 'tr')

    def get_summary_data(self) -> list[SummaryTable]:
        summary_data = []

        for row in self.get_summary_rows():
            cells = row.find_elements(By.TAG_NAME, "td")
            data = SummaryTable(
                name=cells[0].text.split(":")[0].strip(),
                value=Decimal(extract_decimal_price(cells[1].text.strip()))
            )
            summary_data.append(data)
        return summary_data

    def remove_all_products(self):
        while True:
            try:
                remove_buttons = self.driver.find_elements(By.XPATH, "//button[@data-original-title='Remove']")
                if not remove_buttons:
                    break
                remove_buttons[0].click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(remove_buttons[0]))

            except StaleElementReferenceException:
                continue

    def get_content_text(self) -> str:
        content_text = self.driver.find_element(By.ID, 'content')
        return content_text.text
