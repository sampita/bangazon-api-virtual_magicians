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
        fields = ('id', 'merchant_name', 'acct_number', 'expiration_date', 'created_at', 'customer',)
        depth = 2

class PaymentTypes(ViewSet):
    def create(self, request):
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.acct_number = request.data["acct_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]
        new_payment_type.customer_id = request.auth.user.customer.id
        new_payment_type.save()
        
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
            payment_types = payment_types.filter(payment_type__id=payment_type)

        serializer = PaymentSerializer(payment_types, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a  single payment-type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            paymenttype = PaymentType.objects.get(pk=pk)
            paymenttype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)