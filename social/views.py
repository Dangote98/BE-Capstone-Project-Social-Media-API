from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Follow
from .serializers import PostSerializer, ProfileSerializer, FollowSerializer

# Redirect to admin or login depending on user authentication status
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # Redirect authenticated users to admin page
    return redirect('login')

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('posts')  # Redirect to posts or homepage
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Custom pagination for posts
class FeedPagination(PageNumberPagination):
    page_size = 10  # You can set a custom page size here
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional limit on the maximum page size

# View for displaying posts
@login_required
def posts(request):
    posts = Post.objects.all().order_by('-timestamp')  # Display posts in reverse chronological order
    return render(request, 'social/posts.html', {'posts': posts})

# ViewSet for handling Post creation, updates, and deletion
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.values_list('following', flat=True)
        # Show posts from users the current user follows, or their own posts
        return Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    def perform_create(self, serializer):
        # Save the post with the current user as the author
        serializer.save(user=self.request.user)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        # Ensure the user is only allowed to update their own posts
        if post.user != request.user:
            raise PermissionDenied("You can only update your own posts.")
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        # Ensure the user is only allowed to delete their own posts
        if post.user != request.user:
            raise PermissionDenied("You can only delete your own posts.")
        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# ViewSet for handling following/unfollowing users
class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        following_user_id = request.data.get('following')
        following_user = User.objects.get(id=following_user_id)

        if request.user.id == following_user_id:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if created:
            return Response({"message": f"You are now following {following_user.username}."}, status=status.HTTP_201_CREATED)
        return Response({"message": f"You are already following {following_user.username}."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            follow = Follow.objects.get(id=pk, follower=request.user)
            follow.delete()
            return Response({"message": "You have unfollowed the user."}, status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({"error": "You are not following this user."}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        follows = Follow.objects.filter(follower=request.user)
        following_users = [follow.following.username for follow in follows]
        return Response({"following": following_users}, status=status.HTTP_200_OK)

# ViewSet for managing user profiles
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Post update view
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = super().get_object()
        if post.user != self.request.user:
            raise PermissionDenied("You can only update your own posts.")
        return post
