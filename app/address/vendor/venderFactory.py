from .musinsa import Musinsa
from .auction import Auction


class VendorFactory:
    def getVendor(self, vendor_name, **kward):
        # print(kward)
        if vendor_name == 'musinsa':
            return Musinsa(**kward)
        elif vendor_name == 'auction':
            return Auction(**kward)
