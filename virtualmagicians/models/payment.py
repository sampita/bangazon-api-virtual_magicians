from django.db import models
from safedelete.models import HARD_DELETE_NOCASCADE
from safedelete.models import SafeDeleteModel
from .customer import Customer

class PaymentType(SafeDeleteModel):
    # Objects will be hard-deleted, or soft deleted if other objects would have been deleted too.
    _safedelete_policy = HARD_DELETE_NOCASCADE

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="payment_types")
    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    

    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    def __str__(self):
        return f'Customer Id: {self.customer.id}, {self.merchant_name}'
