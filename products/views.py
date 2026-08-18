import logging

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Order, Product

logger = logging.getLogger(__name__)


def _get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def catalog(request):
    category = request.GET.get("category", "")
    products = Product.objects.filter(is_active=True)
    if category in ("ai_agent", "saas_tool"):
        products = products.filter(category=category)
    return render(
        request,
        "products/catalog.html",
        {"products": products, "active_category": category},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    razorpay_order = None
    order = None
    customer_email = request.user.email if request.user.is_authenticated else ""

    if request.method == "POST":
        if not request.user.is_authenticated:
            login_url = reverse("accounts:login")
            return redirect(f"{login_url}?next={request.path}")

        customer_email = request.user.email
        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            messages.error(
                request,
                "Payment is not configured yet. Please contact support.",
            )
        else:
            order = Order.objects.create(
                product=product,
                user=request.user,
                customer_email=customer_email,
                payment_status="pending",
            )
            try:
                client = _get_razorpay_client()
                razorpay_order = client.order.create(
                    {
                        "amount": product.price_in_paise,
                        "currency": "INR",
                        "receipt": f"order_{order.pk}",
                        "notes": {
                            "product_id": str(product.pk),
                            "order_id": str(order.pk),
                            "customer_email": customer_email,
                        },
                    }
                )
                order.razorpay_order_id = razorpay_order["id"]
                order.save(update_fields=["razorpay_order_id"])
            except Exception:
                logger.exception("Failed to create Razorpay order")
                order.payment_status = "failed"
                order.save(update_fields=["payment_status"])
                messages.error(
                    request,
                    "Could not initiate payment. Please try again later.",
                )
                order = None
                razorpay_order = None

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "order": order,
            "razorpay_order": razorpay_order,
            "customer_email": customer_email,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        },
    )


@login_required
@require_POST
def payment_verify(request):
    razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
    razorpay_order_id = request.POST.get("razorpay_order_id", "")
    razorpay_signature = request.POST.get("razorpay_signature", "")

    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        return HttpResponseBadRequest("Missing payment parameters.")

    order = get_object_or_404(
        Order,
        razorpay_order_id=razorpay_order_id,
        user=request.user,
    )

    try:
        client = _get_razorpay_client()
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except razorpay.errors.SignatureVerificationError:
        order.payment_status = "failed"
        order.save(update_fields=["payment_status"])
        messages.error(request, "Payment verification failed. Please contact support.")
        return redirect("products:detail", pk=order.product.pk)
    except Exception:
        logger.exception("Payment verification error")
        messages.error(request, "An error occurred during payment verification.")
        return redirect("products:detail", pk=order.product.pk)

    order.razorpay_payment_id = razorpay_payment_id
    order.payment_status = "paid"
    order.save(update_fields=["razorpay_payment_id", "payment_status"])

    request.session["last_paid_order_id"] = order.pk
    return redirect("products:success")


@login_required
def payment_success(request):
    order_id = request.session.pop("last_paid_order_id", None)
    if not order_id:
        return redirect("products:catalog")
    order = get_object_or_404(
        Order,
        pk=order_id,
        payment_status="paid",
        user=request.user,
    )
    return render(request, "products/success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, payment_status="paid")
    return render(request, "products/my_orders.html", {"orders": orders})
