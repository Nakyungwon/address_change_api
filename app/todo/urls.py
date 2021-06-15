from django.urls import path
from todo import views
# from .views import TodoView

urlpatterns = [
    # path("", TodoView.as_view(), name="index1"),
    path("", views.selectAll, name="all"),
    # path("boot/", views.BootStrap, name="all"),
    path("do/", views.Do, name="do"),
    # path("get/<int:id>", views.selectOne, name="detail"),
    # path("insert", views.insert, name="insert"),
    # path("delete", views.delete, name="delete"),
]
