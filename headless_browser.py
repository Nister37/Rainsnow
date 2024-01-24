import sys
import pyperclip
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class Browser:
    def __init__(self):
        chrome_options = ChromiumOptions()
        chrome_options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())
        # service.creation_flags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.set_page_load_timeout(30)

    def log_in(self, username: str, password: str):
        self.driver.get("https://developer.accuweather.com/user")
        username_field = self.driver.find_element(By.XPATH, "//input[@data-original-title='You may login with either "
                                                            "your assigned username or your e-mail address.']")
        password_field = self.driver.find_element(By.XPATH,
                                                  "//input[@data-original-title='The password field is case "
                                                  "sensitive.']")
        log_in_button = self.driver.find_element(By.ID, "edit-submit--3")

        username_field.send_keys(username)
        password_field.send_keys(password)
        log_in_button.click()

        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "text-muted")))
            return True
        except:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "alert alert-block alert-dismissible alert-danger messages error")))
            return False

    def get_API(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@data-parent='#my-apps-accordion']")))
            self.driver.find_element(By.XPATH, "//a[@data-parent='#my-apps-accordion']").click()

            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.TAG_NAME, 'span"')))
            api_key = self.driver.find_element(By.TAG_NAME, 'span"')

            time.sleep(2)

            action_chains = ActionChains(self.driver)
            action_chains.double_click(api_key).perform()
            action_chains.key_down(Keys.CONTROL).perform()
            action_chains.send_keys('c').perform()
            action_chains.key_up(Keys.CONTROL).perform()

            api_key = pyperclip.paste()

            time.sleep(2)
            return api_key
        except:
            self.create_API()
            self.driver.get("https://developer.accuweather.com/user/me/apps")
            return "Failed"

    def create_API(self):
        self.driver.find_element(By.CLASS_NAME, 'add-app').click()
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "edit-human")))
        self.driver.find_element(By.ID, 'edit-human').send_keys("Snowrain")

        core_weather_select = self.driver.find_elements(By.NAME, 'core_weather')
        core_weather_select[1].click()
        minute_cast_select = self.driver.find_elements(By.NAME, 'minutecast_all')
        minute_cast_select[1].click()

        api_hardware_select = Select(self.driver.find_element(By.ID, 'edit-attribute-where-apis-used'))
        api_hardware_select.select_by_index(1)

        self.driver.find_element(By.NAME, 'attribute_create_with_api[productivityapp]').click()

        programming_language_select = Select(self.driver.find_element(By.ID, 'edit-attribute-programming-language'))
        programming_language_select.select_by_index(6)

        self.driver.find_element(By.ID, 'edit-attribute-business-consumer-b-to-c').click()
        self.driver.find_element(By.ID, 'edit-submit').click()


def main(arg1: str, arg2: str, arg3: str):
    browser = Browser()
    is_logged = browser.log_in(arg1, arg2)

    if is_logged:
        while True:
            API_KEY = browser.get_API()
            if result != "Failed":
                break
    else:
        return "Could not log in! The account might not exist or the network is unstable."

    import time
    time.sleep(60)

    if arg3 == "key_request":
        return API_KEY
    elif arg3 == "weather_request":
        pass


if __name__ == "__main__":
    result = main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)
