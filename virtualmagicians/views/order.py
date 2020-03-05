"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Order, Customer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'customer_id', 'paymenttype_id')


class Orders(ViewSet):

    """Orders for Bangazon"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Products instance
        """
        neworder = Order()
        neworder.customer_id = request.auth.user.customer.id
        neworder.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get the open order for the logged in user/customer
        Returns:
            Response -- JSON serialized list of users
        """      
        orders = Order.objects.filter(customer_id=request.auth.user.customer.id, paymenttype_id=None)
        
        order = self.request.query_params.get('order', None)
        
        if order is not None:
            orders = Order.filter(pk=request.auth.user)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)
