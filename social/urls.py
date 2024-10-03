from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, ProfileViewSet
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'followers', FollowViewSet, basename='follows')  # Specify a basename
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
