from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
    # Built-in Django Admin
    path("django-admin/", admin.site.urls),

    # Main Home Page & CMS App
    path("", home, name="home"),
    path("", include("website_cms.urls")),
    path("labeling/", include("labeling.urls")),
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
