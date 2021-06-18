# from selenium.webdriver.common.keys import Keys
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if platform.system() == 'Darwin':
    chromedriver = '/usr/local/bin/chromedriver'


options = Options()

# options.add_argument('headless')
# options.add_argument('window-size=200x200')
# options.add_argument('lang=ko_KR')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('lang=ko_KR')
# options.add_argument(
#     'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')


options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
options.add_argument(
    "accept=text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
options.add_argument("Referer=https://login.coupang.com/login/login.pang")
options.add_argument("accept-charset=cp1254,ISO-8859-9,utf-8;q=0.7,*;q=0.3")
options.add_argument("accept-encoding=gzip,deflate,sdch")
options.add_argument("accept-language=tr,tr-TR,en-US,en;q=0.8")
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options = webdriver.ChromeOptions(chrome_options=options)
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.delete_all_cookies()

driver.implicitly_wait(3)
id = ''
password = ''
# url = "https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F"
# url = 'https://www.coupang.com/'
url = "https://login.coupang.com/login/login.pang"
driver.get(url)

# time.sleep(3)
# driver.find_element_by_xpath(
#     '/html/body/div[2]/div/article/section/menu[1]/li[1]/a').click()
time.sleep(3)
id_input = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div/form/div[1]/div[1]/div[1]/label/span[2]/input')
driver.execute_script(f"arguments[0].setAttribute('value', '{id}')", id_input)
time.sleep(3)
password_input = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div/form/div[1]/div[2]/div[1]/label/span[2]/input')
driver.execute_script(
    f"arguments[0].setAttribute('value', '{password}')", password_input)
time.sleep(3)
driver.find_element_by_xpath(
    '/html/body/div[1]/div/div/form/div[5]/button').click()
