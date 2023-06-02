from rest_framework import serializers

from data_processing.models import DataFile


class DataFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DataFile
        fields = '__all__'
