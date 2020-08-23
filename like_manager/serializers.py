from rest_framework import serializers
from .models import Like, Dislike

class LikeSerializer(serializers.Serializer):
    class Meta:
        model = Like
        fields = ['user', 'movie']

class DislikeSerializer(serializers.Serializer):
    class Meta:
        model = Dislike
        fields = ['user', 'movie']