from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'followers', FollowViewSet, basename='follows')  # Specify a basename
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
