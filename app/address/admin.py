# from django.contrib.auth import get_user_model
from django.contrib import admin
from address.models import UserInfo
from address.models import RequestVendor
from address.models import Vendor

admin.site.register(UserInfo)
admin.site.register(RequestVendor)
admin.site.register(Vendor)
# # Register your models here.
