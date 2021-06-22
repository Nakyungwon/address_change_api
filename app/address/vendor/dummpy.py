# from selenium.webdriver.common.keys import Keys
import platform
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def input_value(driver, x_path, value):
    input_x_path = driver.find_element_by_xpath(x_path)
    input_x_path.send_keys(value)
    print(input_x_path.getAttribute("value"))
    time.sleep(0.3)

# def enter_input(driver, x_path):
#     driver.find_element_by_xpath(x_path).send_keys(Key.RETURN)


if platform.system() == 'Darwin':
    chromedriver = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
options.add_argument("--profile-directory=Default")
options.add_argument("--whitelisted-ips")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins-discovery")
# options.addArguments(
#     "user-data-dir=/Users/kyungwonna/Library/Application Support/Google/Chrome")
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.delete_all_cookies()
driver.implicitly_wait(3)
url = 'https://my.musinsa.com/login/v1/login?&referer=http%3A%2F%2Fwww.musinsa.com%2Findex.php%3F'
address_url = "https://store.musinsa.com/app/delivery/lists/app/delivery/lists"


driver.get(url)
# user_agent = driver.executeScript("return navigator.userAgent;")
# print(user_agent)

driver.implicitly_wait(3)
# driver.execute_script(
#     "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
# driver.execute_script(
#     "Object.defineProperty(navigator, 'languages', \{get: function() \{return ['ko-KR', 'ko']\}\})")
# driver.execute_script(
#     "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

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
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(
    driver.find_element_by_tag_name("iframe"))
driver.switch_to.frame(
    driver.find_element_by_tag_name("iframe"))
# address_search_x_path = '//*[@id="region_name"]'
element_id = driver.find_element_by_id("region_name")
address_search = os.environ['test_address']
element_id.send_keys(address_search)
element_id.send_keys(Keys.RETURN)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
ul = soup.select_one('ul.list_post')
titles = ul.select('li')
index = 0
for idx, title in enumerate(titles):
    search_address_list = title.attrs['data-addr'].split()
    my_address_search_list = address_search.split()

    if my_address_search_list[-1] == search_address_list[-1] and my_address_search_list[-2] == search_address_list[-2]:
        index = idx

    # print(title.attrs('data-addr'))
index += 1
driver.find_element_by_xpath(
    f'/html/body/div[1]/div/div[2]/ul/li[{index}]/dl/dd[1]/span/button/span[1]').click()

driver.switch_to.window(driver.window_handles[1])
detail_address = '305호'
detail_address_x_path = '/html/body/form/div/table/tbody/tr[5]/td/input[2]'
input_value(driver, detail_address_x_path, detail_address)

driver.switch_to.window(driver.window_handles[1])
default_address = '/html/body/form/div/table/tbody/tr[5]/td/div[2]/input'
driver.find_element_by_xpath(default_address).click()

# 기본 배송지 설정 click
driver.execute_script(
    "document.getElementById('delivery_defaultCheck').click();")
driver.execute_script(
    "document.getElementById('checkTelNone').click();"
)

driver.current_url
register_button = '/html/body/form/div/div/button[2]'
driver.find_element_by_xpath(register_button).click()
