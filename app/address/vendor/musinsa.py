from .base import Base
from .helper import delay
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class Musinsa(Base):
    url = 'https://my.musinsa.com/login/v1/login?&referer=http%3A%2F%2Fwww.musinsa.com%2Findex.php%3F'
    address_url = 'https://store.musinsa.com/app/delivery/lists/app/delivery/lists'
    id_x_path = '/html/body/div/div/form/input[2]'
    password_x_path = '/html/body/div/div/form/input[3]'
    login_button_x_path = '/html/body/div/div/form/button'

    def __init__(
            self,
            id,
            password,
            address,
            address_detail,
            recipient,
            shipping_address,
            phon_number_head,
            phon_number_middle,
            phon_number_tail,
    ):
        super().__init__(self.url, self.address_url)
        # print(self.driver)
        self.driver = webdriver.Chrome(
            executable_path=Base.chromedriver,
            chrome_options=Base.options)
        self.driver.delete_all_cookies()
        self.id = id
        self.password = password
        self.address = address
        self.address_detail = address_detail
        self.recipient = recipient
        self.shipping_address = shipping_address
        self.phon_number_head = phon_number_head
        self.phon_number_middle = phon_number_middle
        self.phon_number_tail = phon_number_tail

    @delay
    def login(self):
        self.input_value(self.id_x_path, self.id)
        self.input_value(self.password_x_path, self.password)
        url = self.click_button(self.login_button_x_path)
        assert url == 'https://www.musinsa.com/index.php'

    @delay
    def open_search_address(self):
        default_address_check = '/html/body/form/div/table/tbody/tr[5]/td/div[1]/button'
        url = self.click_button(default_address_check)
        assert url == 'https://store.musinsa.com/app/mypage/delivery_form'

    @delay
    def search_address(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.switch_to.frame(
            self.driver.find_element_by_tag_name("iframe"))
        self.driver.switch_to.frame(
            self.driver.find_element_by_tag_name("iframe"))
        # address_search_x_path = '//*[@id="region_name"]'
        element_id = self.driver.find_element_by_id("region_name")
        element_id.send_keys(self.address)
        element_id.send_keys(Keys.RETURN)

    @delay
    def select_address(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.select_one('ul.list_post')
        titles = ul.select('li')
        index = 0

        my_address_search_list = self.address.split()
        for idx, title in enumerate(titles):
            search_address_list = title.attrs['data-addr'].split()
            if my_address_search_list[-1] == search_address_list[-1] and my_address_search_list[-2] == search_address_list[-2]:
                index = idx
                break

            # print(title.attrs('data-addr'))
        index += 1
        self.click_button(
            f'/html/body/div[1]/div/div[2]/ul/li[{index}]/dl/dd[1]/span/button/span[1]')

    @delay
    def change_address_base_step(self):
        new_address_x_path = '/html/body/div[1]/a'
        self.click_button(new_address_x_path)

        self.driver.switch_to.window(self.driver.window_handles[-1])

        recipient_x_path = '/html/body/form/div/table/tbody/tr[1]/td/input'
        self.input_value(recipient_x_path, self.recipient)
        shipping_address_x_path = '/html/body/form/div/table/tbody/tr[2]/td/input'
        self.input_value(shipping_address_x_path, self.shipping_address)
        phon_number_head_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[1]'
        self.input_value(phon_number_head_x_path, self.phon_number_head)
        phon_number_middle_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[2]'
        self.input_value(phon_number_middle_x_path, self.phon_number_middle)
        phon_number_tail_x_path = '/html/body/form/div/table/tbody/tr[3]/td/input[3]'
        self.input_value(phon_number_tail_x_path, self.phon_number_tail)
        # 기본 배송지 설정 click
        self.driver.execute_script(
            "document.getElementById('delivery_defaultCheck').click();")
        # 전화번호 없음
        self.driver.execute_script(
            "document.getElementById('checkTelNone').click();")

    def change_address_last_step(self):
        detail_address_x_path = '/html/body/form/div/table/tbody/tr[5]/td/input[2]'
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.input_value(detail_address_x_path, self.address_detail)
        register_button = '/html/body/form/div/div/button[2]'
        self.click_button(register_button)

    def run(self):
        self.open_site()
        self.login()
        self.open_address_page()
        self.change_address_base_step()
        self.open_search_address()
        self.search_address()
        self.select_address()
        self.change_address_last_step()


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
