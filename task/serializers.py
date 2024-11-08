from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    video_input = serializers.CharField(max_length=255, required=True)
    lang = serializers.CharField(max_length=2, required=False, default='en')

    class Meta:
        model = Task
        fields = ('video_input', 'lang', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')