from rest_framework import viewsets, permissions
from .models import Post, Profile, Follow
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer, ProfileSerializer, FollowSerializer

class FeedPagination(PageNumberPagination):
    page_size = 10  # You can set a custom page size here
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional limit on the maximum page size

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() 
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination  # Use the custom pagination class

    def get_queryset(self):
        # Get the posts from the users that the current user follows
        user = self.request.user
        followed_users = user.following.values_list('following', flat=True)
        return Post.objects.filter(user__in=followed_users).order_by('-timestamp')
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

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
    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

