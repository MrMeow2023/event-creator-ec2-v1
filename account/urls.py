from django.urls import path 
from . import views #import from current folder the views.py 

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.edit_profile, name="profile"),
    path("change_pw/", views.PasswordUpdate.as_view(), name="update_password")
]