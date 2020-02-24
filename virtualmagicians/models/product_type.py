from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=55)
    class Meta:
        ordering = ("name", )
        verbose_name = ("names")
        verbose_name_plural = ("names")

