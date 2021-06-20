# from selenium.webdriver.common.keys import Keys
import platform
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def input_value(driver, x_path, value):
    input_x_path = driver.find_element_by_xpath(x_path)
    driver.execute_script(
        f"arguments[0].setAttribute('value', '{value}')",
        input_x_path)
    driver.implicitly_wait(3)


# def enter_input(driver, x_path):
#     driver.find_element_by_xpath(x_path).send_keys(Key.RETURN)


if platform.system() == 'Darwin':
    chromedriver = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
options.addArguments("--profile-directory=Default")
options.addArguments("--whitelisted-ips")
options.addArguments("--start-maximized")
options.addArguments("--disable-extensions")
options.addArguments("--disable-plugins-discovery")
options.addArguments(
    "user-data-dir=/Users/kyungwonna/Library/Application Support/Google/Chrome")
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.delete_all_cookies()
driver.implicitly_wait(3)
# url = "https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F"
# url = 'https://www.coupang.com/'
# url = "https://login.coupang.com/login/login.pang"
# url = "https://front.wemakeprice.com/user/login"
url = 'https://my.musinsa.com/login/v1/login?&referer=http%3A%2F%2Fwww.musinsa.com%2Findex.php%3F'
address_url = "https://store.musinsa.com/app/delivery/lists/app/delivery/lists"


driver.get(url)
driver.implicitly_wait(3)
driver.execute_script(
    "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
driver.execute_script(
    "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
driver.execute_script(
    "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

time.sleep(1)
# id_input = driver.find_element_by_xpath(id_x_path)
# driver.execute_script(f"arguments[0].setAttribute('value', '{id}')", id_input)
id_x_path = '/html/body/div/div/form/input[2]'
password_x_path = '/html/body/div/div/form/input[3]'
login_button_x_path = '/html/body/div/div/form/button'

id = os.environ['test_id']
password = os.environ['test_password']

input_value(driver, id_x_path, id)
input_value(driver, password_x_path, password)
driver.find_element_by_xpath(login_button_x_path).click()
time.sleep(1)

# 주소지 url
driver.get(address_url)
# 신규 주소만들기 open
new_address_x_path = '/html/body/div[1]/a'
driver.find_element_by_xpath(new_address_x_path).click()
driver.implicitly_wait(3)

time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
# 수령인
recipient_x_path = '/html/body/form/div/table/tbody/tr[1]/td/input'
recipient = '나경원'
input_value(driver, recipient_x_path, recipient)


shipping_address_x_path = '/html/body/form/div/table/tbody/tr[2]/td/input'
shipping_address = '우리집'
input_value(driver, shipping_address_x_path, shipping_address)

phon_number_head_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[1]'
phon_number_head = '010'
input_value(driver, phon_number_head_x_path, phon_number_head)
phon_number_middle_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[2]'
phon_number_middle = '9044'
input_value(driver, phon_number_middle_x_path, phon_number_middle)
phon_number_tail_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[3]'
phon_number_tail = '8972'
input_value(driver, phon_number_tail_x_path, phon_number_tail)
# driver.quit()
# 기본주소 체크
default_address_check = '/html/body/form/div/table/tbody/tr[5]/td/div[1]/button'
driver.find_element_by_xpath(default_address_check).click()

time.sleep(1)
driver.switch_to.window(driver.window_handles[2])
driver.switch_to.frame(
    driver.find_element_by_tag_name("iframe"))
driver.switch_to.frame(
    driver.find_element_by_tag_name("iframe"))
# address_search_x_path = '//*[@id="region_name"]'
element_id = driver.find_element_by_id("region_name")
address_search = os.environ['test_address']
element_id.send_keys(address_search)
element_id.send_keys(Keys.RETURN)


address_x_path = '/html/body/form/div/table/tbody/tr[5]/td/div[1]/button'
driver.find_element_by_xpath(address_x_path).click()
