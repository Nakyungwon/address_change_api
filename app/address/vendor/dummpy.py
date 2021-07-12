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
driver.implicitly_wait(5)
url = 'https://memberssl.auction.co.kr/Authenticate'
address_url = 'https://memberssl.auction.co.kr/AddressBook/AddAddressBook.aspx'
driver.get(url)
driver.implicitly_wait(3)
time.sleep(1)
id_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/ul/li[1]/input'
password_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/ul/li[2]/input'
login_button_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/button[1]'
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

driver.switch_to.window(driver.window_handles[-1])
# 수령인
recipient_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[3]/div[2]/input'
recipient = '나경원'
input_value(driver, recipient_x_path, recipient)
shipping_address_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[2]/div[2]/input'
shipping_address = '우리집'
input_value(driver, shipping_address_x_path, shipping_address)
aa = driver.find_element_by_xpath(shipping_address_x_path)
aa.clear()

# phon_number_head_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[1]'
phon_number_head = '010'
# input_value(driver, phon_number_head_x_path, phon_number_head)
# phon_number_middle_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[2]'
phon_number_middle = '9044'
# input_value(driver, phon_number_middle_x_path, phon_number_middle)
# phon_number_tail_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[3]'
phon_number_tail = '8972'
# input_value(driver, phon_number_tail_x_path, phon_number_tail)
phon_number_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[4]/div[2]/input'
input_value(
    driver,
    phon_number_x_path,
    phon_number_head +
    phon_number_middle +
    phon_number_tail)

# driver.quit()
# 기본주소 체크
# default_address_check = '/html/body/form/div/table/tbody/tr[5]/td/div[1]/button'
# driver.find_element_by_xpath(default_address_check).click()
driver.switch_to.window(driver.window_handles[-1])
address_search_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[5]/button'
driver.find_element_by_xpath(address_search_x_path).click()

driver.switch_to.frame(
    driver.find_element_by_tag_name("iframe"))
address_search_x_path = '/html/body/div[2]/div/div/div/div[1]/div[1]/div[1]/form/input'
address_search = os.environ['test_address']
input_value(
    driver,
    address_search_x_path,
    address_search)

input_value(
    driver,
    address_search_x_path,
    Keys.RETURN)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
ul = soup.select_one('ul.lst_search')
titles = ul.select('li.list_item')
index = 0
for idx, title in enumerate(titles):
    # search_address_list = title.attrs['data-addr'].split()
    search_address_list = title.select_one('p.tx_addr').get_text().split()
    my_address_search_list = address_search.split()

    if my_address_search_list[-1] == search_address_list[-1] and my_address_search_list[-2] == search_address_list[-2]:
        index = idx

    # print(title.attrs('data-addr'))
index += 1
driver.find_element_by_xpath(
    f'/html/body/div[2]/div/div/div/div[1]/div[6]/div/ul/li[{index}]/a[2]').click()
# driver.switch_to.window(driver.window_handles[-1])
# driver.find_element(
#     '/html/body/div[2]/div/div/div/div[1]/div[4]/div/a').click()
driver.find_element_by_css_selector("a.btn_set").click()

driver.switch_to.window(driver.window_handles[-1])
detail_address = '305호'
detail_address_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[6]/div[2]/input'
input_value(driver, detail_address_x_path, detail_address)

# driver.current_url
register_button = '/html/body/form/div[3]/div/div/section/div[2]/button[2]'
driver.find_element_by_xpath(register_button).click()
