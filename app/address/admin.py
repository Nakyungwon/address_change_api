from django.contrib import admin
from address.models import User
from address.models import RequestVendor
from address.models import Vendor

admin.site.register(User)
admin.site.register(RequestVendor)
admin.site.register(Vendor)
# Register your models here.
