from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("<int:pk>/", views.product_detail, name="detail"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),
    path("payment/success/", views.payment_success, name="success"),
]
