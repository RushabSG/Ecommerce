from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):

    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex="^(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$",
                message="Enter valid mobile number",
            )
        ],
    )
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=100, null=True, blank=True)

    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self) -> str:
        return "Shipping Address - " + str(self.pk)


class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Order - #" + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Order Item - #" + str(self.id)
