from django.test import TestCase
from .vendor.musinsa import Musinsa

# Create your tests here.


class YourTestClass(TestCase):
    def test_address(self):
        import os
        id = os.environ['test_id']
        password = os.environ['test_password']
        address = os.environ['test_address']
        obj = Musinsa(
            id,
            password,
            address,
            '305호',
            '나경원',
            '우리집',
            '010',
            '9044',
            '8972')
        obj.run()
