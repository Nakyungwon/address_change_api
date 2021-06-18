# import platform
# from selenium import webdriver

# if platform.system() == 'Darwin':
#     chromedriver = '/usr/local/bin/chromedriver'

# driver = webdriver.Chrome(chromedriver)

# driver.get('https://www.coupang.com/')
from base import Base
import time
# import common


class coupang(Base):
    url = 'https://login.coupang.com/login/login.pang'

    # def __init__(self):
    # url = 'https://www.coupang.com/'

    # def run(self):
    # self.open_site()
    def login_click(self):
        time.sleep(5)
        # self.driver.find_element_by_xpath('//a[@class="login"]').click()
        # self.driver.find_element_by_xpath('//a[@class="login"]').click()

        input = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/form/div[1]/div[1]/div[1]/label/span[2]/input')
        self.driver.execute_script(
            "arguments[0].setAttribute('value', 'new value!')", input)

        # self.driver.find_element_by_xpath('//login-password-input'
        # self.driver.find_element_by_xpath('//button[@class="login__button login__button - -submit _loginSubmitButton"]').click()

    def run(self):
        self.open_site()
        self.login_click()


if __name__ == '__main__':
    obj = coupang()
    # common.test()
    obj.run()
