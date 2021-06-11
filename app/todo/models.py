from django.db import models
# Create your models here.

class Todo(models.Model):
    class Meta:
        db_table = 'todo' 

    t_task = models.CharField(max_length=100)

    def __str__(self):
        return self.t_task