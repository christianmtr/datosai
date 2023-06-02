from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.api.serializers import UserAddAPIkeySerializer


@api_view(['PATCH'])
def add_openai_api_key(request):
    serializer = UserAddAPIkeySerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
