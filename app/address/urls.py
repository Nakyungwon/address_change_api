from django.urls import path
from address import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.render_login, name="login"),
    path("address", views.address, name="address"),
]
