<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
=======
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
<<<<<<< HEAD
    # Built-in Django Admin
    path("django-admin/", admin.site.urls),

    # Main Home Page & CMS App
    path("", home, name="home"),
    path("", include("website_cms.urls")),
=======
    path("admin/", admin.site.urls),
    path("", home, name="home"),
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
    path("labeling/", include("labeling.urls")),
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
]
<<<<<<< HEAD

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
