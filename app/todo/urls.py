from django.urls import path
from todo import views

urlpatterns = [
    path("all/", views.selectAll, name="index"),
    path("get/", views.selectOne, name="index"),
    path("insert/", views.insert, name="index"),
    path("delete/", views.delete, name="index"),
]
