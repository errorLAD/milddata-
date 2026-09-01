from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.catalog, name="catalog"),
<<<<<<< HEAD
    path("saas/", views.saas_directory, name="saas_directory"),
    path("saas/<slug:slug>/", views.saas_detail, name="saas_detail"),
    path("saas/<slug:slug>/launch/", views.saas_launch, name="saas_launch"),
    path("detail/", views.catalog, name="detail_index"),
    path("detail/<str:identifier>/", views.universal_product_detail, name="universal_detail"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("book-demo/", views.book_demo, name="book_demo"),
=======
    path("my-orders/", views.my_orders, name="my_orders"),
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
    path("<int:pk>/", views.product_detail, name="detail"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),
    path("payment/success/", views.payment_success, name="success"),
]
