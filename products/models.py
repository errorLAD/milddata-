from django.conf import settings
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("ai_agent", "AI Agent"),
        ("saas_tool", "SaaS Tool"),
    ]
    BILLING_TYPE_CHOICES = [
        ("one_time", "One-time"),
        ("monthly", "Monthly"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    features = models.TextField(
        blank=True,
        help_text="One feature per line",
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_type = models.CharField(max_length=20, choices=BILLING_TYPE_CHOICES)
    access_info = models.TextField(
        blank=True,
        help_text="Shown to customer after successful payment",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_features_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    @property
    def price_display(self):
        suffix = "/mo" if self.billing_type == "monthly" else ""
        return f"₹{self.price:,.0f}{suffix}"

    @property
    def price_in_paise(self):
        return int(self.price * 100)


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )
    customer_email = models.EmailField()
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.product.name} ({self.payment_status})"
