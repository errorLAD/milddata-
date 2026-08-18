from django.contrib import admin

from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "billing_type",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "billing_type", "is_active")
    search_fields = ("name", "description")
    list_editable = ("is_active",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "customer_email",
        "payment_status",
        "razorpay_order_id",
        "created_at",
    )
    list_filter = ("payment_status", "product__category", "created_at")
    search_fields = (
        "customer_email",
        "user__email",
        "razorpay_order_id",
        "razorpay_payment_id",
    )
    readonly_fields = (
        "product",
        "user",
        "customer_email",
        "razorpay_order_id",
        "razorpay_payment_id",
        "created_at",
    )
