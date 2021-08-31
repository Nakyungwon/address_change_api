from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from address.vendor.helper import delay, myassert
from .base import Base
from tenacity import retry, stop_after_attempt
import time

from address.errors.consumer_exceptions import LoginException
# import sys
# print(sys.path)
# from address.erros.consumer_exceptions import *


class Coupang(Base):
    display_name = '쿠팡'
    url = 'https://login.coupang.com/login/login.pang'
    address_url = 'https://memberssl.auction.co.kr/AddressBook/AddAddressBook.aspx'
    id_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/ul/li[1]/input'
    password_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/ul/li[2]/input'
    login_button_x_path = '/html/body/div[2]/div/div/form/div/div/div/div[1]/fieldset/button[1]'

    def __init__(
            self,
            **kward
    ):
        super().__init__(self.url, self.address_url)
        # self.driver.delete_all_cookies()
        self.vendor_id = kward['vendor_id']
        self.vendor_password = kward['vendor_password']
        self.address = kward['address']
        self.address_detail = kward['address_detail']
        self.recipient = kward['recipient']
        self.shipping_address = kward['shipping_address']
        self.phone_number_head = kward['phone_number_head']
        self.phone_number_middle = kward['phone_number_middle']
        self.phone_number_tail = kward['phone_number_tail']

    @delay
    def login(self):
        self.input_value(self.id_x_path, self.vendor_id)
        self.input_value(self.password_x_path, self.vendor_password)
        self.click_button(self.login_button_x_path)

        is_login = super().is_get_cookie('auction')
        assert is_login is True or myassert(LoginException)
        # assert url == 'https://www.musinsa.com/index.php'

    @delay
    def open_search_address(self):
        default_address_check = '/html/body/form/div[3]/div/div/section/div[1]/div[5]/button'
        self.click_button(default_address_check)
        # assert url == 'https://store.musinsa.com/app/mypage/delivery_form'

    @delay
    def search_address(self):
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.switch_to.frame(
            self.driver.find_element_by_tag_name("iframe"))
        # address_search_x_path = '//*[@id="region_name"]'
        address_search_x_path = '/html/body/div[2]/div/div/div/div[1]/div[1]/div[1]/form/input'
        self.input_value(address_search_x_path, self.address)
        self.input_value(address_search_x_path, Keys.RETURN, is_confirm=False)

    # @retry(stop=stop_after_attempt(3))
    @delay
    def get_tag_value(self, count=0):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.select_one('ul.lst_search')
        titles = ul.select('li.list_item')
        if len(titles) == 0 and count < 4:
            count += 1
            time.sleep(3)
            print(titles)
            return self.get_tag_value(count)
        else:
            return titles

    @delay
    def select_address(self):
        index = 0
        titles = self.get_tag_value()

        my_address_search_list = self.address.split()
        for idx, title in enumerate(titles):
            search_address_list = title.select_one(
                'p.tx_addr').get_text().split()
            if my_address_search_list[-1] == search_address_list[-1] and my_address_search_list[-2] == search_address_list[-2]:
                index = idx
                break
        index += 1
        self.click_button(
            f'/html/body/div[2]/div/div/div/div[1]/div[6]/div/ul/li[{index}]/a[2]')
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector("a.btn_set").click()

    @delay
    def change_address_base_step(self):
        # new_address_x_path = '/html/body/div[1]/a'
        # self.click_button(new_address_x_path)

        self.driver.switch_to.window(self.driver.window_handles[-1])
        recipient_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[3]/div[2]/input'
        self.input_value(recipient_x_path, self.recipient, is_reset=True)
        shipping_address_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[2]/div[2]/input'
        self.input_value(
            shipping_address_x_path,
            self.shipping_address,
            is_reset=True)
        phon_number_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[4]/div[2]/input'
        self.input_value(
            phon_number_x_path,
            self.phone_number_head + '-' +
            self.phone_number_middle + '-' +
            self.phone_number_tail)

    def change_address_last_step(self):
        detail_address_x_path = '/html/body/form/div[3]/div/div/section/div[1]/div[6]/div[2]/input'
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.input_value(detail_address_x_path, self.address_detail)
        register_button = '/html/body/form/div[3]/div/div/section/div[2]/button[2]'
        self.click_button(register_button)

    def execute_login_page(self):
        self.login()
        self.open_address_page()
        return True, "로그인 성공"

    def execute_address_page(self):
        self.change_address_base_step()
        self.open_search_address()
        self.search_address()
        self.select_address()
        self.change_address_last_step()
        return True, "주소변경 성공"

    def run(self):
        self.open_site()
        self.execute_login_page()
        self.execute_address_page()


# if __name__ == "__main__":
#     import os
#     id = os.environ['test_id']
#     password = os.environ['test_password']
#     address = os.environ['test_address']
#     obj = Musinsa(
#         id,
#         password,
#         address,
#         '305호',
#         '나경원',
#         '우리집',
#         '010',
#         '9044',
#         '8972')
#     obj.run()
