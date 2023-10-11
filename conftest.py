import yaml
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

with open("config.yaml", encoding="utf-8") as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]


@pytest.fixture(scope="module")
def browser():
    """
    Инициализирует вебдрайвер
    :return: драйвер браузера firefox или chrome в зависимости от параметра browser
    """
    if browser == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        # service = Service(executable_path=ChromeDriverManager().install())
        service = Service(testdata["driver_path"])
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
