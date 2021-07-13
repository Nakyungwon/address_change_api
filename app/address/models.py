from django.db import models

# Create your models here.


class UserInfo(models.Model):
    class Meta:
        db_table = 'user_info'

    user_id = models.CharField(max_length=20, primary_key=True)
    user_password = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    address_detail = models.CharField(max_length=200, null=True)
    recipient = models.CharField(max_length=200, null=True)
    shipping_address = models.CharField(max_length=200, null=True)
    phon_number_head = models.CharField(max_length=200, null=True)
    phon_number_middle = models.CharField(max_length=200, null=True)
    phon_number_tail = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)


class RequestVendor(models.Model):
    class Meta:
        db_table = 'request_vendor'
        unique_together = (("user_id", "vendor_pk"),)
    # t_task = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    vendor_pk = models.IntegerField()
    vendor_id = models.CharField(max_length=200, null=True)
    vendor_password = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return


class Vendor(models.Model):
    class Meta:
        db_table = 'vendor'

    # t_task = models.CharField(max_length=100)
    vendor_pk = models.CharField(max_length=100, null=True)
    vendor_nm = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return
