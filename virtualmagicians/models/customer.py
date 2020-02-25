from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.expressions import F

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=55)
    # last_name = models.CharField(max_length=55)
    # email = models.CharField(max_length=55)
    # created_at = models.DateTimeField()
    # is_active = models.BooleanField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)
        #Instances of F() act as a reference to a model field within a query. These references can then be used in query filters to compare the values of two different fields on the same model instance.
        
        #In this case, order by the date the user joined (by ascending) and null fields last.