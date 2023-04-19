import subprocess
import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from parameterized import parameterized
import logging
import sys

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.ajaxsystems',
    appActivity='.ui.activity.LauncherActivity',
    language='en',
    locale='US',
    autoGrantPermissions=True
)

appium_server_url = 'http://localhost:4723'


def get_udid():
    output = subprocess.check_output(['adb', 'devices']).decode()
    devices = output.strip().split('\n')[1:]
    for device in devices:
        if 'device' in device:
            udid = device.split('\t')[0]
            return udid


class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger()
        cls.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        cls.logger.addHandler(handler)

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)
        self.driver.implicitly_wait(10)
        udid = get_udid()
        self.logger.info(f'Starting test case on device with udid:"{udid}"')

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_positive_login(self) -> None:
        self.login("qa.ajax.app.automation@gmail.com", "qa_automation_password")

        self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/actionbar')

        self.logger.info('Test "test_positive_login" passed')

    @parameterized.expand([
        ("invalid_email_format", "invalid_email", "any_password", "Invalid email format"),
        ("wrong_password_or_login", "login@gmail.com", "invalid_password", "Wrong login or password")
    ])
    def test_negative_login(self, name, email, password, expected_message) -> None:
        self.login(email, password)

        snackbar = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/snackbar_text')
        self.assertEquals(snackbar.text, expected_message)

        self.logger.info(f'Test "{name}" passed with message "{expected_message}"')

    def login(self, email, password):
        enter_button = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/login')
        enter_button.click()

        password_field = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/password')
        password_field.send_keys(password)

        email_field = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/login')
        email_field.send_keys(email)

        login_button = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/next')
        login_button.click()
