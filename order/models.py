from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class DeliveryLocation(models.Model):
    pincode = models.CharField(max_length=256, null=True, blank=True)
    pickup_charge = models.DecimalField(
        default=0, null=True, blank=True, max_digits=20, decimal_places=2
    )
    delivery_charge = models.DecimalField(
        default=0, null=True, blank=True, max_digits=20, decimal_places=2
    )
    is_active = models.BooleanField(default=False)


class Order(models.Model):
    class OrderType(models.TextChoices):
        delivery = ("delivery", "Delivery")
        pickup = ("pickup", "Pickup")

    class OrderStatus(models.TextChoices):
        pending = ("pending", "Pending")
        completed = ("completed", "Completed")
        cancelled = ("cancelled", "Cancelled")
        rejected = ("rejected", "Rejected")

    class PaymentMethod(models.TextChoices):
        cash = ("cash", "Cash")
        upi = ("upi", "Upi")
        card = ("card", "Card")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey("cart.Cart", on_delete=models.CASCADE)
    address = models.ForeignKey("accounts.Address", on_delete=models.CASCADE)
    ref = models.UUIDField(default="", null=True, blank=True, unique=True)
    order_type = models.CharField(default=OrderType.delivery, max_length=56)
    order_status = models.CharField(default=OrderStatus.pending, max_length=56)
    payment_method = models.CharField(default=PaymentMethod.cash, max_length=56)
    total_price = models.DecimalField(
        null=True, blank=True, default=0, max_digits=20, decimal_places=2
    )
    total_discount = models.DecimalField(
        null=True, blank=True, default=0, max_digits=20, decimal_places=2
    )

    def update_order_price(self):
        total_cart_price = 0
        total_cart_discount = 0
        # calculating total cart price and total cart discount
        lines = self.cart.lines.all()
        for line in lines:
            total_cart_price += line.price
            total_cart_discount += line.discount
        self.total_discount = total_cart_discount
        self.save()

        total_price = total_cart_price
        delivery_location_charge, created = DeliveryLocation.objects.get_or_create()
        # adding delivery or pickup charges
        if self.order_type == Order.OrderType.delivery:
            total_price += delivery_location_charge.delivery_charge
        elif self.order_type == Order.OrderType.pickup:
            total_price += delivery_location_charge.pickup_charge

        self.total_price = total_price
        self.save()
