from django.db import models
from .customer import Customer
from .payment import PaymentType

class Order(models.Model):
    
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="orders")
    # what is related_name? -SP
    payment = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, related_name="payment_types")
    created_at = models.DateTimeField()    
    class Meta:
        ordering = ("created_at", )
        verbose_name = ("order")
        verbose_name_plural = ("orders")


    def __str__(self):
        return f'''
        Order: {self.id} 
        Customer: {self.customer.user.first_name} {self.customer.user.last_name}
        '''