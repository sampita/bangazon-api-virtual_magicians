"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description', 'quantity', 'location', 'image_path', 'created_at', 'customer_id', 'product_type_id')
        depth = 2


class Products(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """

        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park products resource

        Returns:
            Response -- JSON serialized list of park products
        """

        products = Product.objects.all()

        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     products = products.filter(area__id=area)

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data)