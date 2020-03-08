"""View module for handling requests about products"""
import json
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Order, Product, Customer, OrderProduct
from .product import ProductSerializer

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
        fields = ('id', 'url', 'createdAt', 'customer', 'payment_type',)
        depth = 2


class Orders(ViewSet):

    """Orders for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle get request for 1 order
        Returns:
            Response -- JSON serialized order instance
        """

        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
        Response -- JSON serialized Products instance
        """
        open_order = Order.objects.filter(customer_id=request.auth.user.customer.id, paymenttype=None)
        req_body = json.loads(request.body.decode())
        if open_order is not None:
            print(open_order)
            add_to_order = OrderProduct()
            add_to_order.order_id = open_order.order.id
            add_to_order.product_id = req_body['product_id']
            add_to_order.save()

        else:
            neworder = Order()
            neworder.customer_id = request.auth.user.customer.id
            neworder.save()

            new_orderproduct = OrderProduct()
            new_orderproduct.order_id = neworder.id
            new_orderproduct.product_id = req_body['product_id']
            new_orderproduct.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get the open order for the logged in user/customer
        Returns:
            Response -- JSON serialized list of users
        """      
        orders = Order.objects.filter(customer_id=request.auth.user.customer.id, payment_type_id=None)
        
        order = self.request.query_params.get('order', None)
        
        if order is not None:
            orders = Order.filter(pk=request.auth.user)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)
    
        ################# SHOPPING CART ###############################
    # Example request:
    #   http://localhost:8000/orders/cart
    @action(methods=['get'], detail=False)
    def cart(self, request):
        current_user = Customer.objects.get(user=request.auth.user)
        try:
            open_order = Order.objects.get(customer=current_user, payment_type=None)
            products_on_order = Product.objects.filter(cart__order=open_order)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(products_on_order, many=True, context={'request': request})
        return Response(serializer.data)
