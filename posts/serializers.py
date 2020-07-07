from django.conf import settings
from rest_framework import serializers
from .models import Post

MAX_POST_LENGTH = settings.MAX_POST_LENGTH

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_POST_LENGTH:
            raise serializers.ValidationError("This post is too long")
        return value