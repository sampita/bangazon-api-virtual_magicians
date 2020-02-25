"""Park Areas for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtualmagicians.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products
    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'theme')


class ListProducts(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Product instance
        """
        newarea = Product()
        newarea.name = request.data["name"]
        newarea.customer = request.data["customer"]
        newarea.price = request.data["price"]
        newarea.description = request.data["description"]
        newarea.quantity = request.data["quantity"]
        newarea.location = request.data["location"]
        newarea.image_path = request.data["image_path"]
        newarea.created_at = request.data["created_at"]
        newarea.save()

        serializer = ProductSerializer(newarea, context={'request': request})

        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single park area
    #     Returns:
    #         Response -- JSON serialized park area instance
    #     """
    #     try:
    #         area = ParkArea.objects.get(pk=pk)
    #         serializer = ParkAreaSerializer(area, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a park area
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     area = ParkArea.objects.get(pk=pk)
    #     area.name = request.data["name"]
    #     area.theme = request.data["theme"]
    #     area.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single park area
    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         area = ParkArea.objects.get(pk=pk)
    #         area.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except ParkArea.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     """Handle GET requests to park areas resource
    #     Returns:
    #         Response -- JSON serialized list of park areas
    #     """
    #     areas = ParkArea.objects.all()
    #     serializer = ParkAreaSerializer(
    #         areas, many=True, context={'request': request})
    #     return Response(serializer.data)