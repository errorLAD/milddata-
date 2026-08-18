from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("labeling/", include("labeling.urls")),
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
]
