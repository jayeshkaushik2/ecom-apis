from email.quoprimime import unquote
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.conf import settings

# Create your models here.
class Cart(models.Model):
    class Status(models.TextChoices):
        open = ("open", "Open")
        submitted = ("submitted", "Submitted")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ref = models.UUIDField(default=uuid4, null=True, blank=True, unique=True)
    status = models.CharField(max_length=56, default=Status.open)

class CartLine(models.Model):
    product = models.ForeignKey("product_items.Product", on_delete=models.CASCADE)
    ref = models.UUIDField(default="", null=True, blank=True, unique=False)
    # line_ref = models.CharField(max_length=56, null=True, blank=True, unique=True)
    cart = models.ForeignKey("cart.Cart", on_delete=models.DO_NOTHING, related_name="lines")
    quantity = models.PositiveIntegerField(null=True, blank=True, default=1)
    discount = models.DecimalField(
        null=True, blank=True, max_digits=20, decimal_places=2
    )
    price = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)

    def set_price(self):
        discount = 0
        if self.product.discount_pct is not None:
            discount = (self.product.price * self.product.discount_pct) / 100
            self.discount = self.quantity * discount
        price = self.quantity * (self.product.price - discount)
        self.price = price
        self.save()

    def set_line_ref(self):
        pass