# Author: Sam Pita
# Purpose: This file is the User serializer as well as manages User retrieve requests

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

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