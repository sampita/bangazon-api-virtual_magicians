from django.db import models
from .customer import Customer

class PaymentType(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="payment_types")
    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=25)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField()
    

    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    def __str__(self):
        return f'Customer Id: {self.customer_id}, {self.merchant_name}'
