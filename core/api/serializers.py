from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    openai_api_key = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserAddAPIkeySerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('openai_api_key', )
