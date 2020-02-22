from django.db import models
from .customer import Customer

class Product(models.Model):

    name = models.CharField(max_length=50)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="products")
    price = models.DecimalField(max_digits=6, decimal_places=2)