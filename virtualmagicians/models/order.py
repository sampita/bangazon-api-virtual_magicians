from django.db import models
from .customer import Customer
from .payment import PaymentType

class Order(models.Model):
    
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="orders")
    # related_name is nickname you can call this by later -SP
    payment = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, related_name="payment_type", null=True)
    created_at = models.DateTimeField()
    
    class Meta:
        ordering = ("created_at", )