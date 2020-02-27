# Author: Sam Pita
# Purpose: This file is the Payment Type serializer as well as manages all Payment Type database requests

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import PaymentType

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='payment',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number', 'expiration_date', 'customer_id', 'created_at')
        depth = 2
    
    class PaymentTypes(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    