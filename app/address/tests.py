from django.test import TestCase
# from .vendor.musinsa import Musinsa
import os
import time
from address.vendor.coupang import Coupang
from address.models import UserInfo, RequestVendor, Vendor

# Create your tests here.


class CoupangTest(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     id = os.environ['test_id']
    #     password = os.environ['test_password']
    #     address = os.environ['test_address']
    #     coupang_obj = Coupang(
    #         vendor_id=id,
    #         vendor_password=password,
    #         address=address,
    #         address_detail='305호',
    #         recipient='나경원',
    #         shipping_address='우리집',
    #         phone_number_head='010',
    #         phone_number_middle='9044',
    #         phone_number_tail='8972')
    
    def test_login_page(self):
        id = os.environ['test_id']
        password = os.environ['test_password']
        address = os.environ['test_address']
        coupang_obj = Coupang(
            vendor_id=id,
            vendor_password=password,
            address=address,
            address_detail='305호',
            recipient='나경원',
            shipping_address='우리집',
            phone_number_head='010',
            phone_number_middle='9044',
            phone_number_tail='8972')
        coupang_obj.open_site()
        time.sleep(10)
        self.assertTrue(True)
