from django.db import models
# from .customer import Customer
from .payment import PaymentType

class Order(models.Model):
    """this is a doc string - go away blue squiggly"""
    
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING, related_name="orders")
    # related_name is nickname you can call this by later -SP

    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name="payment_type", null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ("created_at", )