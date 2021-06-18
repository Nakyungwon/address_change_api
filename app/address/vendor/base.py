import platform
from selenium import webdriver


class Base:
    # def __init__(self):
    if platform.system() == 'Darwin':
        chromedriver = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver)

    # def open_site(cls):

    @classmethod
    def open_site(cls):
        # self.driver.get('https://www.coupang.com/')
        # print('aaaa')
        print(cls.url)
        cls.driver.get(cls.url)    
