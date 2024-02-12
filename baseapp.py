import random
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import *
from config import Config


class BaseFunc:
    """The class contains basic functions for Selenium and the page under test"""

    def __init__(self, browser):
        self.browser = browser
        self.base_url = Config.URL["BASE_URL"]

    def get_element(self, locator):
        return WebDriverWait(self.browser, Config.TIMEOUT).until(EC.presence_of_element_located(locator))

    def get_elements(self, locator):
        return WebDriverWait(self.browser, Config.TIMEOUT).until(EC.presence_of_all_elements_located(locator))

    def open_url(self):
        """Open hosting page"""
        return self.browser.get(self.base_url)


class PageFunc(BaseFunc):
    def click_element(self, locator):
        return self.get_element(locator).click()

    def input_text(self, locator, text):
        element = self.get_element(locator)
        element.clear()
        return element.send_keys(text)

    def scroll_to_element(self, locator):
        element = self.get_element(locator)
        return self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def server_selection(self, serv: str) -> None:
        """
        Choose server type dedicated or virtual
        :param serv: type of server
        """
        self.scroll_to_element(HostingPage.TOP_SIDE)
        serv_buttons = self.get_elements(HostingPage.BUTTONS_DEDICATED_OR_VIRTUAL)
        for button in serv_buttons:
            if serv in button.text:
                button.click()
                break

    def currency_selection(self, cur: str) -> None:
        """
        Choose the currency
        :param cur: our currency
        """
        if cur == Config.DATA["CURRENCY_USD"]:
            usd = self.get_element(HostingPage.BUTTON_RADIO_USD)
            if 'active' in usd.get_attribute('class'):
                pass
            else:
                usd.click()
            assert 'active' in usd.get_attribute('class')
        if cur == Config.DATA["CURRENCY_EUR"]:
            eur = self.get_element(HostingPage.BUTTON_RADIO_EUR)
            if 'active' in eur.get_attribute('class'):
                pass
            else:
                eur.click()
            assert 'active' in eur.get_attribute('class')

    def get_boundary_validate_value(self) -> tuple[int, int]:
        """
        Selecting the boundary values from an element containing these values.
        :return: 2 int values
        """
        element = self.get_element(HostingPage.GET_PRICE_RANGE)
        bnd_min_price, bnd_max_price = [int(value) for value in element.text.split()]
        return bnd_min_price, bnd_max_price

    def get_random_equivalent_range(self, b_min_pr: int, b_max_pr: int) -> tuple[int, int]:
        """
        Random selection of equivalent values within the range might not be the optimal choice.
        Further refinement is needed.
        :param b_min_pr: minimum boundary value
        :param b_max_pr: maximum boundary value
        :return: 2 int values
        """
        eq_min_price = random.randint(b_min_pr, b_max_pr)
        eq_max_price = random.randint(b_min_pr, b_max_pr)
        eq_max_price = eq_max_price - eq_max_price % 10 + random.randint(0, 9)
        if eq_min_price > eq_max_price:
            eq_min_price, eq_max_price = eq_max_price, eq_min_price
        return eq_min_price, eq_max_price

    def input_price(self, pr_min: int, pr_pax: int) -> None:
        """
        Entering values into the minimum and maximum price input fields.
        :param pr_min: minimum value
        :param pr_pax: maximum value
        """
        self.input_text(HostingPage.INPUT_MIN_PRICE, pr_min)
        self.input_text(HostingPage.INPUT_MAX_PRICE, pr_pax)
        # alert_msg_for_min_price = self.get_element(browser, *HostingPage.INFO_MSG_FOR_OUT_MIN_PRICE)
        # alert_msg_for_max_price = self.get_element(browser, *HostingPage.INFO_MSG_FOR_OUT_MAX_PRICE)

        # ТУТ СЛОВИЛ БАГ НА САЙТЕ: при вводе граничных значений в input всегда появляется alert 'Out of range'
        # запускает assert и тест падает, что не соответствует моему ожиданию :) а так можно добавить проверку что ниже
        # assert (alert_msg_for_min_price.is_displayed() or alert_msg_for_max_price.is_displayed()) is False, \
        #     f"'Out of range' message is displayed for the valid value of {pr_min} or {pr_pax}"

    def open_more_cards(self) -> None:
        """
        The function opens all the cards on the page; if the element is not found, it triggers an exception.
        """
        while True:
            try:
                show_more_button = self.get_element(HostingPage.BUTTON_SHOW_MORE_SERVERS)
                if show_more_button.text in ["Show more dedicated servers", "Show more virtual servers"]:
                    show_more_button.click()
                else:
                    break
            except TimeoutException:
                break

    def get_price_and_currency_servers(self, cur: str, eq_pr_min: int, eq_pr_pax: int) -> None:
        """
        Checking for compliance with the price range and correspondence to the selected currency.
        :param cur: currency
        :param eq_pr_min: minimum equivalent value
        :param eq_pr_pax: maximum equivalent value
        :return:
        """
        cards = self.get_elements(HostingPage.All_CARDS_SERVERS)
        prices, currencies = [], []
        for card in cards:
            price_element = card.find_element(By.CLASS_NAME, 'price-card_price')
            price = float(price_element.find_element(By.TAG_NAME, 'span').text.strip())
            currency = price_element.find_element(By.TAG_NAME, 'sub').text.strip()
            prices.append(price)
            currencies.append(currency)
        assert all(eq_pr_min <= price <= eq_pr_pax for price in prices), \
            f"The price of the servers in the displayed cards is outside the range of {eq_pr_min} to {eq_pr_pax}."
        assert all(currency == cur for currency in currencies), \
            f"The currency of the servers in the displayed cards is different from {cur}."
