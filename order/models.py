from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Address
from cart.models import Cart


# Create your models here.
class DeliveryLocation(models.Model):
    pincode = models.CharField(max_length=256, null=True, blank=True)
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
        received = ("received", "Received")
        received_at_warehouse = ("received_at_warehouse", "Received_at_warehouse")
        out_for_delivery = ("out_for_delivery", "Out_for_delivery")
        completed = ("completed", "Completed")
        returned = ("returned", "Returned")
        exchange = ("exchange", "Exchange")

    class PaymentMethod(models.TextChoices):
        cash = ("cash", "Cash")
        upi = ("upi", "Upi")
        card = ("card", "Card")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        "cart.Cart", on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.ForeignKey(
        "accounts.Address", on_delete=models.CASCADE, null=True, blank=True
    )
    ref = models.UUIDField(default="", null=True, blank=True, unique=True)
    order_type = models.CharField(default=OrderType.delivery, max_length=56)
    order_status = models.CharField(default=OrderStatus.pending, max_length=56)
    payment_method = models.CharField(default=PaymentMethod.cash, max_length=56)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    received_at = models.DateTimeField(blank=True, null=True)
    out_for_delivery_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)
    exchange_at = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(
        null=True, blank=True, default=0, max_digits=20, decimal_places=2
    )
    total_discount = models.DecimalField(
        null=True, blank=True, default=0, max_digits=20, decimal_places=2
    )

    def set_order_address(self):
        address = Address.objects.filter(user=self.user).first()
        if address is not None:
            self.address = address

    def can_orderprice_be_updated(self):
        if self.address is None and self.order_type == Order.OrderType.delivery:
            return False, "address is not provided"

        if self.cart.lines.all().count() <= 0:
            return False, "no item present in the cart"

        return True, ""

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

    def can_be_placed(self):
        """
        1. check for delivery address (valid or not)(deliverable or not)
        2. check if items present or not in cart
        3. check for total price is zero or not
        4. etc.
        """
        if self.order_status not in [Order.OrderStatus.pending]:
            return False, "order is already placed"

        if self.address is None:
            return False, "address is not provided"

        delivery_location = DeliveryLocation.objects.filter(
            pincode=self.address.pincode, is_active=True
        ).first()

        if delivery_location is None:
            return False, "order is not deliverable at the given address"

        if self.cart.lines.all().count() <= 0:
            return False, "no item present in the cart"

        if self.total_price <= 0:
            return False, "order price is not set"
        return True, ""

    def place_order(self):
        self.order_status = Order.OrderStatus.received
        self.cart.status = Cart.Status.submitted
        self.cart.save()
        self.received_at = timezone.now()