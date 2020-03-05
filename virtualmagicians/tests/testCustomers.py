from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from virtualmagicians.models.product_type import ProductType

class TestCustomer(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)


    def test_get_producttype(self):
        """test to get  a payment type from the API"""

        new_product_type = ProductType.objects.create(
            user=self.user,
            name='product made',
        )

        #use the client to send the request and store the response
        response = self.client.get(reverse('product_type-list'), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Getting 200 back because we have a success url

        self.assertEqual(response.status_code, 200)

