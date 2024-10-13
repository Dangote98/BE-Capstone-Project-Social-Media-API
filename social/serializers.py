from rest_framework import serializers
from .models import Post, Follow, Profile
from django.contrib.auth.models import User

# Serializer for displaying user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer for Posts
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Display username instead of user ID

    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'timestamp', 'media']

# Serializer for Follow relationships
class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'following']

# Serializer for User Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # To include user data with profile

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']
