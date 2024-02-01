from selenium.webdriver.common.by import By


class HostingPage:
    """This class contains locators for the page with the same name."""
    BUTTON_RADIO_EUR = (By.CSS_SELECTOR, '#left')
    BUTTON_RADIO_USD = (By.CSS_SELECTOR, '#right')
    BUTTONS_DEDICATED_OR_VIRTUAL = (By.CSS_SELECTOR, ".gc-server-configurator-buttons button")
    GET_PRICE_RANGE = (By.CSS_SELECTOR, ".multi-range-labels")
    INPUT_MIN_PRICE = (By.CSS_SELECTOR, "[formcontrolname='min'] input")
    INPUT_MAX_PRICE = (By.CSS_SELECTOR, "[formcontrolname='max'] input")
    INFO_MSG_FOR_OUT_MIN_PRICE = (By.CSS_SELECTOR, "[formcontrolname='min'] p.gc-input-validation")
    INFO_MSG_FOR_OUT_MAX_PRICE = (By.CSS_SELECTOR, "[formcontrolname='max'] p.gc-input-validation")
    BUTTON_SHOW_MORE_SERVERS = (By.CSS_SELECTOR, ".gc-server-configurator-more")
    All_CARDS_SERVERS = (By.CSS_SELECTOR, ".price-card")
    TOP_SIDE = (By.CSS_SELECTOR, ".gc-small-m-top_x-large")
