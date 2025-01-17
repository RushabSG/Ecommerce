from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("complete-checkout/", views.complete_checkout, name="complete-checkout"),
    path("payment-success/", views.payment_success, name="payment-success"),
    path("payment-failed/", views.payment_failed, name="payment-failed"),
]
