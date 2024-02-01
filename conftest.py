import pytest
import requests
from selenium import webdriver
import time


@pytest.fixture(scope="session")
def browser(timeout=15):
    """The fixture checks if Chrome is running in the Docker container, then proceeds to open the browser."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(options=options)
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "120.0")
    url_chrome = "http://chrome:4444/wd/hub"
    url_status_page = "http://chrome:4444/wd/hub/status"
    while True:
        try:
            res = requests.get(url_status_page)
            if res.status_code == 200 or timeout == 0:
                break
        except requests.exceptions.ConnectionError as e:
            print(e)
        time.sleep(1)
        timeout -= 1
    driver = webdriver.Remote(command_executor=url_chrome,
                              options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
