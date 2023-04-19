import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from parameterized import parameterized

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


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    @parameterized.expand([
        ("valid_credentials", "qa.ajax.app.automation@gmail.com", "qa_automation_password", True),
        ("invalid_email", "invalid_email", "qa_automation_password", False),
        ("invalid_password", "qa.ajax.app.automation@gmail.com", "invalid_password", False)
    ])
    def test_login(self, name, email, password, expected_result) -> None:
        el = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/login')
        el.click()

        password_field = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/password')
        password_field.send_keys(password)

        email_field = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/login')
        email_field.send_keys(email)

        login_button = self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/next')
        login_button.click()

        self.driver.find_element(by=AppiumBy.ID, value='com.ajaxsystems:id/actionbar')


if __name__ == '__main__':
    unittest.main()
