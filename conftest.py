import yaml
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from send_report_to_email import send_message_to_email

with open("testdata.yaml") as f:
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


# def pytest_terminal_summary(terminalreporter, exitstatus):
def pytest_sessionfinish(session, exitstatus):
    """
    Отправляет отчет о тестировании после завершения теста
    """
    send_message_to_email(testdata['fromaddr_report'],
                          testdata['toaddr_report'],
                          testdata['mail_password'],
                          "report.html")
