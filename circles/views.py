# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
# App Models
from circles.models import Circle
# App Serializers
from circles.serializers import CircleSerializer


@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.all()
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    serializer = CircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
