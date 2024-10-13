from django.contrib import admin
from .models import Post, Follow, Profile
from django.core.exceptions import ValidationError

# Admin configuration for the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')  # Display user, bio, and profile picture
    search_fields = ('user__username', 'bio')  # Enable search by username and bio
    list_filter = ('user__username',)  # Filter by username

# Admin configuration for the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp', 'media', 'media_type')  # Display media URL and type
    search_fields = ('content', 'user__username')  # Enable search by content and username
    list_filter = ('timestamp', 'media_type')  # Filter by timestamp and media type
    ordering = ('-timestamp',)  # Order posts by latest timestamp

    # Override save_model to add logic for post updates
    def save_model(self, request, obj, form, change):
        # Ensure only the post owner can update their post
        if change and obj.user != request.user:
            raise ValidationError("You can only update your own posts.")
        super().save_model(request, obj, form, change)

# Admin configuration for the Follow model
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')  # Display the follower and following users
    search_fields = ('follower__username', 'following__username')  # Search by usernames
    list_filter = ('follower__username', 'following__username')  # Filter by follower and following usernames

    # Override save_model to prevent users from following themselves
    def save_model(self, request, obj, form, change):
        if obj.follower == obj.following:
            raise ValidationError("Users cannot follow themselves.")
        super().save_model(request, obj, form, change)

    # Custom admin action to bulk unfollow selected users
    actions = ['unfollow_selected_users']

    def unfollow_selected_users(self, request, queryset):
        count = queryset.count()
        queryset.delete()  # Perform bulk unfollow
        self.message_user(request, f"Successfully unfollowed {count} users.")
    unfollow_selected_users.short_description = "Unfollow selected users"
