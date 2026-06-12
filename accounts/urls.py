from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.placeholder, name="placeholder"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("login/google/", views.google_login, name="google_login"),
    path("login/google/callback/", views.google_callback, name="google_callback"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]
