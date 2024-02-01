import allure
import pytest
from flaky import flaky
from locators import *
from functions import *


class TestUI:
    @classmethod
    def setup_class(cls):
        cls.base_func = BaseFunc()

    @allure.epic("TestUI")
    @allure.feature("Open hosting page")
    @allure.title("Start chrome and open page")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag('browser')
    @allure.description("Checking the page opening.")
    def test_url(self, browser):
        url = "https://gcore.com/hosting"
        self.base_func.open_url(browser, url)
        with (allure.step(f"Check url")):
            assert url == browser.current_url

    @allure.epic("TestUI")
    @allure.feature("Test for hosting calculator")
    @allure.title("Check calculating for {server} servers with '{currency}' currency")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag('hosting')
    @allure.description("Choose server type dedicated or virtual, choose the currency, enter price min and max values, "
                        "input equivalent values, expand of server selection cards, verification of all cards for "
                        "compliance with prices in the equivalent range and the selected currency.")
    @flaky(max_runs=3, min_passes=1)
    @pytest.mark.parametrize("server, currency", [('Virtual', '€'),
                                                  ('Virtual', '$'),
                                                  ('Dedicated', '€'),
                                                  ('Dedicated', '$')],
                             ids=("virtual_EUR", "virtual_USD", "dedicated_EUR", "dedicated_USD"))
    def test_for_hosting_calculator(self, browser, server, currency):
        with allure.step(f"Choose server type {server}"):
            self.base_func.server_selection(browser, server)
        with allure.step(f"Choose the currency '{currency}'"):
            self.base_func.currency_selection(browser, currency)
        bnd_min_price, bnd_max_price = self.base_func.get_boundary_validate_value(browser)
        with allure.step(f"Used the boundary values: {bnd_min_price}, {bnd_max_price}"):
            self.base_func.input_price(browser, bnd_min_price, bnd_max_price)
        eq_min_price, eq_max_price = self.base_func.get_random_equivalent_range(bnd_min_price, bnd_max_price)
        with allure.step(f"Used the equivalent values: {eq_min_price}, {eq_max_price}"):
            self.base_func.input_price(browser, eq_min_price, eq_max_price)
        with allure.step(f"All server cards are opened"):
            self.base_func.open_more_cards(browser)
        with allure.step(f"Checking {server} server cards for prices in the range from {eq_min_price} "
                         f"to {eq_max_price} and '{currency}' currency"):
            self.base_func.get_price_and_currency_servers(browser, currency, eq_min_price, eq_max_price)
