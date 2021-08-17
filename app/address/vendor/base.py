import platform
from tenacity import retry, stop_after_attempt
from selenium import webdriver
from abc import ABC, abstractmethod
from address.vendor.helper import delay, myassert
from address.errors.consumer_exceptions import SiteEnterException


class Base(ABC):
    # def __init__(self):
    if platform.system() == 'Darwin':
        chromedriver = '/usr/local/bin/chromedriver'
    else:
        # Todo
        pass
    options = webdriver.ChromeOptions()
    options.add_argument('lang=ko_KR')
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-gpu")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--whitelisted-ips")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")

    def __init__(self, url, address_url):
        self.url
        self.address_url
        self.driver = webdriver.Chrome(
            executable_path=Base.chromedriver,
            chrome_options=Base.options)
        self.driver.delete_all_cookies()
    
    # @classmethod
    @delay
    def open_site(self):
        self.driver.get(self.url)
        assert self.url in self.driver.current_url or myassert(SiteEnterException)
        return True, '사이트 진입'

    # @classmethod
    @delay
    def open_address_page(self):
        self.driver.get(self.address_url)
        assert self.address_url in self.driver.current_url or myassert(SiteEnterException("주소창 진입 실패"))

    @retry(stop=stop_after_attempt(3))
    def input_value(self, x_path, value, is_reset=False, is_confirm=True):
        x_path_element = self.driver.find_element_by_xpath(x_path)
        if is_reset:
            x_path_element.clear()
        x_path_element.send_keys(value)
        if is_confirm and self.confirm_input_value(x_path_element) != value:
            raise
        else:
            return value

    @delay
    def confirm_input_value(self, element):
        value = element.get_attribute('value')
        return value

    def click_button(self, x_path):
        self.driver.find_element_by_xpath(x_path).click()
        return self.driver.current_url
    
    def get_tag_value(self, x_path):
        self.driver.find_element_by_xpath(x_path).click()
        return self.driver.current_url

    def set_dummy_javascript(self):
        self.driver.implicitly_wait(3)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        self.driver.execute_script(
            "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    def is_get_cookie(self, key):
        cookies = self.driver.get_cookies()
        value = sum(list(map(lambda x: x['name'] == key, cookies)))
        return value > 0
        
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def run(self):
        pass
