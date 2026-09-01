from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
<<<<<<< HEAD
    path("guest/", views.guest_login, name="guest_login"),
=======
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
    path("logout/", views.logout_view, name="logout"),
]
