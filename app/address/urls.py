from django.urls import path
from address import views

urlpatterns = [
    path("", views.index, name="index"),
    path("room", views.room, name="room"),
    path("health", views.health, name="health"),
    path("signin_page", views.render_signin, name="signin_page"),
    path("signup_page", views.render_signup, name="signup_page"),
    path("userinfo_page", views.render_user_info, name="userinfo_page"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("update_address", views.update_address, name="update_address"),
    path("vendor_request", views.vendor_request, name="vendor_request")
]