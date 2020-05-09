from rest_framework import serializers
from user_management.models import FileSystem
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class FileSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSystem
        fields = ['title', 's3_file_url', 'file_type']
