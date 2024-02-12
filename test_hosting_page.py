import allure
import pytest
from flaky import flaky
from baseapp import *
from config import Config


@allure.epic("TestUI")
@allure.feature("Test for hosting calculator")
@allure.title("Check calculating for {server} servers with '{currency}' currency")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag('hosting')
@allure.description("Choose server type dedicated or virtual, choose the currency, enter price min and max values, "
                    "input equivalent values, expand of server selection cards, verification of all cards for "
                    "compliance with prices in the equivalent range and the selected currency.")
@flaky(max_runs=3, min_passes=1)
@pytest.mark.parametrize("server, currency", [(Config.DATA["SERVER_1"], Config.DATA["CURRENCY_EUR"]),
                                              (Config.DATA["SERVER_1"], Config.DATA["CURRENCY_USD"]),
                                              (Config.DATA["SERVER_2"], Config.DATA["CURRENCY_EUR"]),
                                              (Config.DATA["SERVER_2"], Config.DATA["CURRENCY_USD"])],
                         ids=("virtual_EUR", "virtual_USD", "dedicated_EUR", "dedicated_USD"))
def test_for_hosting_calculator(browser, server, currency):
    hosting_page = PageFunc(browser)
    with (allure.step(f"Check url")):
        hosting_page.open_url()
    with allure.step(f"Choose server type {server}"):
        hosting_page.server_selection(server)
    with allure.step(f"Choose the currency '{currency}'"):
        hosting_page.currency_selection(currency)
    bnd_min_price, bnd_max_price = hosting_page.get_boundary_validate_value()
    with allure.step(f"Used the boundary values: {bnd_min_price}, {bnd_max_price}"):
        hosting_page.input_price(bnd_min_price, bnd_max_price)
    eq_min_price, eq_max_price = hosting_page.get_random_equivalent_range(bnd_min_price, bnd_max_price)
    with allure.step(f"Used the equivalent values: {eq_min_price}, {eq_max_price}"):
        hosting_page.input_price(eq_min_price, eq_max_price)
    with allure.step(f"All server cards are opened"):
        hosting_page.open_more_cards()
    with allure.step(f"Checking {server} server cards for prices in the range from {eq_min_price} "
                     f"to {eq_max_price} and '{currency}' currency"):
        hosting_page.get_price_and_currency_servers(currency, eq_min_price, eq_max_price)
