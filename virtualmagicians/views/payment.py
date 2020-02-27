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
        fields = ('id', 'merchant_name', 'acct_number', 'expiration_date', 'customer_id', 'created_at')
        depth = 2

class PaymentTypes(ViewSet):
    def create(self, request):
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.acct_number = request.data["acct_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]
        new_payment_type.customer_id = request.auth.user.customer.id
        new_payment_type.created_at = request.data["created_at"]
        
        serializer = PaymentSerializer(new_payment_type, context={'request': request})

        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to Payment Types resource
        Returns:
            Response -- JSON serialized list of Payment Types
        """

        payment_types = PaymentType.objects.all()

        payment_type = self.request.query_params.get('payment_type', None)
        if payment_type is not None:
            payment_types = payment_types.filter(paymenttype__id=payment_type)

        serializer = PaymentSerializer(payment_types, many=True, context={'request': request})

        return Response(serializer.data)