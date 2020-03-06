# Author: Sam Pita
# Purpose: This file is the Customer serializer as well as manages all Customer database requests

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Customer
from rest_framework.decorators import action

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'user',)
        depth = 2
        
class Customers(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            customer = request.auth.user.customer       
            # customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to customers resource
        Returns:
            Response -- JSON serialized list of customers
        """      
        customers = Customer.objects.filter(id = request.auth.user.customer.id)

        customer = self.request.query_params.get('customer', None)

        if customer is not None:
            customers = customers.filter(id=customer)

        serializer = CustomerSerializer(customers, many=True, context={'request': request})

        return Response(serializer.data)

    #Custom action to update user profile
    @action(methods=['put'], detail=False)
    def profile_update(self, request):
        """
        Handle PUT requests for a customer
        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=request.auth.user.customer.id)
        # customer.user.id = request.auth.user.customer.id
        customer.address = request.data["address"]
        # accesses the nested users last name
        customer.user.last_name = request.data["last_name"]
        customer.user.first_name = request.data["first_name"]
        customer.save()
        customer.user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)