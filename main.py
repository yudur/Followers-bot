
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

import time

import os
import dotenv

dotenv.load_dotenv()


class FirefoxDriver:
    def __init__(self) -> None:
        self.options = FirefoxOptions()
        self.driver = Firefox(options=self.options)

    def open_website(self, url: str) -> None:
        if type(url) != str:
            raise TypeError("The url parameter must be a str")
        else:
            self.driver.get(url)

    def login(self) -> None:
        running = True

        while running:
            try:
                self.driver.implicitly_wait(10)
                self.driver.find_element(By.ID, "username").send_keys(os.getenv("EMAIL_LIKE4LIKE"))
                self.driver.find_element(By.ID, "password").send_keys(os.getenv("PASSWORD_LIKE4LIKE"))
                time.sleep(1)
                self.driver.find_element(
                    By.XPATH,
                    '//*[@id="login"]/fieldset/table/tbody/tr[8]/td/span'
                ).click()

                try:
                    self.driver.find_element(By.ID, "username").send_keys("")
                    self.driver.find_element(By.ID, "password").send_keys("")
                    time.sleep(.5)
                except:
                    running = False
                    continue
            except:
                running = False

    def main(self) -> None:
        self.open_website("https://www.like4like.org/")

        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[3]/a').click()

        self.login()

        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[3]/a').click()

        self.driver.find_element(By.ID, "select-feature").click()
        self.driver.find_element(By.XPATH, '//*[@id="select-feature"]/option[24]').click()

if __name__ == "__main__":
    driver = FirefoxDriver()
    driver.main()