from django.urls import path
from address import views

urlpatterns = [
    path("", views.index, name="index"),
    path("room", views.room, name="room"),
    path("signin_page", views.render_signin, name="signin_page"),
    path("signup_page", views.render_signup, name="signup_page"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
]