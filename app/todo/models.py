from django.db import models
import datetime
# Create your models here.


class Todo(models.Model):
    class Meta:
        db_table = 'todo'

    # t_task = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, null=True)
    task = models.TextField(null=True)
    highlight = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    # created_at = models.DateTimeField(
    #     default=datetime.datetime.now(), null=True, blank=True)  # 해당 레코드 생성시 현재 시간 자동저장
    # updated_at = models.DateTimeField(
    #     default=datetime.datetime.now(), null=True, blank=True)

    def __str__(self):
        return self.task
