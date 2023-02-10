from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.proxy import Proxy, ProxyType

import pyautogui

import time

import os
import dotenv

dotenv.load_dotenv()  # loading the env

# TODO: proxy apenas se nescessaria
# myProxy = "20.111.54.16:80"

# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'ftpProxy': myProxy,
#     'sslProxy': myProxy,
#     'noProxy': '' # set this value as desired
#     })


# class responsible for the logic of the program 
class FirefoxDriver:
    def __init__(self) -> None:
        self.options = FirefoxOptions()  # loads browser options
        self.driver = Firefox(options=self.options)  # initialize the webdriver

    # opens the url in the browser and if the parameter 
    # is not a string it raises a TypeError
    def open_website(self, url: str) -> None:
        if type(url) != str:
            raise TypeError("The url parameter must be a str")
        else:
            self.driver.get(url)

    # function responsible for logging in to Like4Like.
    # If the user does not log in, it resets the data and 
    # tries to log in again, when logged in, the repetition loop ends.
    def login_like4like(self) -> None:
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

    def __send_password(self) -> None:
        self.driver.implicitly_wait(10)
        
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"
        ).send_keys(os.getenv("PASSWORD_TWITTER"))

        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div"
        ).click()

    # log in to twitter
    def login_twitter(self) -> None:
        # get current window handle
        current_tab = self.driver.current_window_handle
        # get first child window
        chwd = self.driver.window_handles

        for w in chwd:
            # switch focus to child window
            if (w != current_tab):
                self.driver.switch_to.window(w)
                break
        
        # self.driver.maximize_window()

        self.driver.implicitly_wait(25)
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/span/span/span"
        ).click()

        self.driver.implicitly_wait(25)
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"
        ).send_keys(os.getenv("EMAIL_TWITTER"))
        
        self.driver.implicitly_wait(25)
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div"
        ).click()


        try:
            self.__send_password()
        except:
            self.driver.implicitly_wait(25)
            self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"
            ).send_keys(os.getenv("USERNAME_TWITTER"))

            self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div"
            ).click()

            self.__send_password()

    def follow(self) -> None:
        running = True
        while running:
            try:
                time.sleep(1)
                imgButton = pyautogui.locateCenterOnScreen("images/program/followButton1.png", confidence=0.7)  # type: ignore
                pyautogui.click(imgButton.x, imgButton.y)
                running = False
            except:
                continue

    # main function
    def main(self) -> None:
        # opening the Like4Like website
        self.open_website("https://www.like4like.org/")

        # accessing the login page
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[3]/a').click()

        self.login_like4like()

        # opening the free credits page
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[3]/a').click()

        # selecting the method of earning credits
        self.driver.find_element(By.ID, "select-feature").click()
        self.driver.find_element(By.XPATH, '//*[@id="select-feature"]/option[24]').click()

        self.driver.implicitly_wait(10)
        self.driver.find_element(
            By.XPATH,
            '/html/body/div[6]/div/div[1]/div[2]/div[2]/div[4]/div[1]/div[2]/div[1]/div/div[3]/div/div/a'
        ).click()

        self.login_twitter()
        self.follow()

        # confirm that you followed
        
        # self.driver.implicitly_wait(8)
        # self.driver.find_element(
            # By.XPATH,
            # "/html/body/div[6]/div/div[1]/div[2]/div[2]/div[4]/div[1]/div[2]/div[1]/div/div[1]/a"
        # ).click()


if __name__ == "__main__":
    driver = FirefoxDriver()
    driver.main()
