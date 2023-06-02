from openai.error import OpenAIError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import UserHasApiKeyPermission
from data_processing.api.serializers import DataFileSerializer
from data_processing.models import DataFile
from data_processing.openai_utils import get_data, compose_prompt, check_prompt_length, send_request_to_openai


class DataFileViewSets(viewsets.ModelViewSet):
    serializer_class = DataFileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = DataFile.objects.filter(user=user)
        return queryset

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated, UserHasApiKeyPermission])
    def file_description(self, request, pk=None):
        user = request.user
        data_file = self.get_object()  # the database record
        csv_file = data_file.csv
        csv_data = get_data(csv_file)
        prompt = compose_prompt(csv_data)
        check_prompt_length(prompt)

        try:
            response = send_request_to_openai(prompt, user.openai_api_key)
        except OpenAIError as err:
            return Response({"error": str(err)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data_file.response = response
            data_file.save()
            return Response({"description": response}, status=status.HTTP_200_OK)
