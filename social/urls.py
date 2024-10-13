from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, ProfileViewSet, signup, home_redirect
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

# Function to handle redirection based on authentication
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # Redirect authenticated users to admin page
    else:
        return redirect('/login/')  # Redirect unauthenticated users to login page

# Set up router for ViewSets
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'followers', FollowViewSet, basename='follows')
router.register(r'profiles', ProfileViewSet)

# URL patterns for the app
urlpatterns = [
    path('', home_redirect, name='home_redirect'),  # Redirect to login/admin based on authentication
    path('api/', include(router.urls)),  # API endpoints (for posts, followers, profiles)
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),  # Redirect logged-in users
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),  # Path for user signup
]
