import pytest
from selenium import webdriver
import requests
import time


@pytest.fixture(scope="session")
def browser(wait=15):
    """The fixture checks if Chrome is running in the Docker container, then proceeds to open the browser."""
    use_docker = False
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if use_docker:
        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", "120.0")
        url_local_chrome = "http://chrome:4444/wd/hub"
        url_status_page = "http://chrome:4444/wd/hub/status"
        while True:
            try:
                echo = requests.get(url_status_page)
                if echo.status_code == 200 or wait == 0:
                    break
            except requests.exceptions.ConnectionError as e:
                print(e)
            time.sleep(1)
            wait -= 1
        driver = webdriver.Remote(command_executor=url_local_chrome,
                                  options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()
