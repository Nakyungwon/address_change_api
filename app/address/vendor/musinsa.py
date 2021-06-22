from base import Base
import helper


class Musinsa(Base):
    url = 'https://my.musinsa.com/login/v1/login?&referer=http%3A%2F%2Fwww.musinsa.com%2Findex.php%3F'
    id_x_path = '/html/body/div/div/form/input[2]'
    password_x_path = '/html/body/div/div/form/input[3]'
    login_button_x_path = '/html/body/div/div/form/button'

    address_url = 'https://store.musinsa.com/app/delivery/lists/app/delivery/lists'

    def __init__(self, id, password, address, address_detail):
        self.id = id
        self.password = password
        self.address = address
        self.address_detail = address_detail

    @helper.delay
    def login(self):
        self.input_value(self.id_x_path, self.id)
        self.input_value(self.password_x_path, self.password)
        pass

    def run(self):
        self.open_site()
        self.login()


if __name__ == "__main__":
    import os
    id = os.environ['test_id']
    password = os.environ['test_password']
    address = os.environ['test_address']
    obj = Musinsa(id, password, address, '305호')
    obj.run()
