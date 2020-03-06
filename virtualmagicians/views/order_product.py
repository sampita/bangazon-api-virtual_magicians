"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import OrderProduct, Order

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = OrderProduct()
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id')
        depth = 2


class OrderProducts(ViewSet):

    """Products on Open Order for Bangazon"""

    def create(self, request):
        """Handle POST operations to add product to order
        Returns:
            Response -- JSON serialized Products instance
        """
        product_to_add_to_order = OrderProduct()
        product_to_add_to_order.customer_id = request.auth.user.customer.id
        product_to_add_to_order.save()

        serializer = OrderProductSerializer(product_to_add_to_order, context={'request': request})

        return Response(serializer.data)

    # def list(self, request):
    #     """Handle GET requests to get all products from the user's open order
    #     Returns:
    #         Response -- JSON serialized list of users
    #     """      
        
    #     # get open order
    #     order = Order.objects.filter(customer_id=request.auth.user.customer.id, paymenttype_id=None)
        
    #     # products = OrderProduct.objects.filter(customer_id=request.auth.user.customer.id, paymenttype_id=None)
        
    #     product = self.request.query_params.get('orderproduct', None)
        
    #     if order is not None:
    #         products = OrderProduct.filter(pk=request.auth.user)

    #     serializer = OrderProductSerializer(orders, many=True, context={'request': request})

    #     return Response(serializer.data)
