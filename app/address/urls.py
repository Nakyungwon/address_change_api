from django.urls import path
from address import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.render_login, name="login"),
    path("address", views.address, name="address"),
    path("room", views.room, name="room"),
    path("signup", views.render_signup, name="signup"),
    # path("test", views.test, name="test"),
]
