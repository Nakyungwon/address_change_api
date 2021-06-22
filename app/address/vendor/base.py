import platform
from tenacity import retry, stop_after_attempt
from selenium import webdriver
from abc import ABC, abstractmethod
import helper


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
    driver = webdriver.Chrome(
        executable_path=chromedriver,
        chrome_options=options)
    driver.delete_all_cookies()

    @classmethod
    @helper.delay
    def open_site(cls):
        Base.driver.get(cls.url)

    @retry(stop=stop_after_attempt(3))
    def input_value(self, x_path, value):
        x_path_element = self.driver.find_element_by_xpath(x_path)
        x_path_element.send_keys(value)
        if self.confirm_input_value(x_path_element) != value:
            raise
        else:
            return value

    @helper.delay
    def confirm_input_value(self, element):
        value = element.get_attribute('value')
        return value

    def set_dummy_javascript(self):
        self.driver.implicitly_wait(3)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        self.driver.execute_script(
            "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def run(self):
        pass
