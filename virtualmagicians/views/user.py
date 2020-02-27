# Author: Sam Pita
# Purpose: This file is the User serializer as well as manages User retrieve requests

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from virtualmagicians.models import Customer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)
        
class Users(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user instance
        """

        try:
            user = Customer.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to users resource
        Returns:
            Response -- JSON serialized list of users
        """      
        users = User.objects.all()
        profile = self.request.query_params.get('profile', None)
        
        current_user = Customer.objects.get(user=request.auth.user)
        
        if profile is not None:
            users = User.filter(pk=request.auth.user)

        serializer = UserSerializer(users, many=True, context={'request': request})

        return Response(serializer.data)