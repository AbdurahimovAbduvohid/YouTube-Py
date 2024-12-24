from rest_framework import serializers
from users.models import CustomUser
from .models import Video, Comment, LikeDislike


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'file', 'low_quality', 'high_quality', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'created_at', 'video']


class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    class Meta:
        model = LikeDislike
        fields = ['id', 'user', 'video', 'is_like']


class VideoDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeDislikeSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'file', 'processed_file',
            'low_quality', 'high_quality', 'created_at', 'is_active',
            'comments', 'likes', 'like_count', 'dislike_count'
        ]

    def get_like_count(self, obj):
        return obj.likes.filter(is_like=True).count()

    def get_dislike_count(self, obj):
        return obj.likes.filter(is_like=False).count()