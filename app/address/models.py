from django.db import models

# Create your models here.


class Address(models.Model):
    class Meta:
        db_table = 'address'

    # t_task = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    detail_address = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return


class Service(models.Model):
    class Meta:
        db_table = 'service'

    # t_task = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return
