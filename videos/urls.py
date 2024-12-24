from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, CommentViewSet, LikeDislikeViewSet

router = DefaultRouter()
router.register('videos', VideoViewSet, basename='video')
router.register('comments', CommentViewSet)
router.register('likes_dislikes', LikeDislikeViewSet)

urlpatterns = [
    path('videos/<int:pk>/details/', VideoViewSet.details, name='video-details'),
    path('', include(router.urls)),
]
