from django.urls import path
from todo import views
# from .views import TodoView

urlpatterns = [
    # path("", TodoView.as_view(), name="index1"),
    path("all", views.selectAll, name="all"),
    # path("get/<int:id>", views.selectOne, name="detail"),
    # path("insert", views.insert, name="insert"),
    # path("delete", views.delete, name="delete"),
]
