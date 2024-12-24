from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Video, Comment, LikeDislike
from .serializers import VideoSerializer, CommentSerializer, LikeDislikeSerializer, VideoDetailSerializer
from .tasks import process_video


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        video = serializer.save(user=self.request.user)
        # using celery
        process_video.delay(video.id)

    @action(detail=True, methods=['post'])
    def reprocess(self):
        video = self.get_object()
        process_video.delay(video.id)
        return Response({'status': 'Video processing started'})

    @action(detail=True, methods=['get'])
    def details(self, pk=None):
        try:
            self.get_object()
            video = Video.objects.prefetch_related(
                'comments',
                'likes'
            ).get(id=pk)

            serializer = VideoDetailSerializer(video)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response(
                {'error': 'Video not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
