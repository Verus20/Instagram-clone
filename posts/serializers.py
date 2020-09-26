from django.conf import settings
from rest_framework import serializers
from .models import Post, PostLike, Test

MAX_POST_LENGTH = settings.MAX_POST_LENGTH
POST_ACTION_OPTIONS = settings.POST_ACTION_OPTIONS

'''
Serializers return data from a queryset and transform the data into native
python data types. Can be used through Django REST Framework.
Similar to how data for a post is handled by the forms.py file
'''
# Serializer for getting data from an action made on a post by a user
# Actions can include liking, unliking, commenting, or uncommenting on a post
class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # turn values from "Like " -> "like"
        if not value in POST_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for posts")
        return value

# Serializer for creating posts
class PostCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'likes']
    
    def get_likes(self, obj):
        return obj.likes.count()

    # Make sure a post isn't too long or the post isn't longer than 2200 characters
    # value for max post length is found in the settings.py folder with the variable called MAX_POST_LENGTH
    def validate_content(self, value):
        if len(value) > MAX_POST_LENGTH:
            raise serializers.ValidationError("This post is too long")
        return value

# Serializer for getting data from a post made by a user
class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = PostCreateSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'likes', 'is_comment', "parent"]
    
    def get_likes(self, obj):
        return obj.likes.count()

# Serializer for getting data from a like made on a post by a user
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'post_id', 'user_id']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'text', 'time', 'integer']
