from django.db import models
from .order import Order
from .product import Product

class OrderProduct(models.Model):


    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="cart")

    class Meta:
        ordering = ("order_id", )
        verbose_name = ("OrderProduct")
        verbose_name_plural = ("OrderProducts")
