from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Order, OrderProduct, Customer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'created_at', 'customer', 'payment_type_id )
        depth = 2

class Orders(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(Order_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to order
        Returns:
            Response -- JSON serialized list of order
        """
       orders = Order.objects.all()
       customer_id = request.auth.user.customer.id

        logged_in_customer = self.request.query_params.get('customer', False)
        if logged_in_customer == 'true':
            orders = orders.filter(customer__id=customer_id)

        open_order = self.request.query_params.get('open', False)
        if open_order == 'true':
            orders = orders.filter(payment_type__id=None)

        serializer = OrderSerializer(
           orders,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for an order
        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.payment_type_id = request.data["payment_type_id"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)