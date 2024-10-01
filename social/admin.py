from django.contrib import admin
from .models import Post, Follow
from django.contrib import messages
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('content',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')

    # Override the save_model method to prevent self-following in the admin interface
    def save_model(self, request, obj, form, change):
        # Prevent a user from following themselves
        if obj.follower == obj.following:
            raise ValidationError("Users cannot follow themselves.")
        super().save_model(request, obj, form, change)

    # Optional: Add a custom action to "unfollow" directly from the admin interface
    actions = ['unfollow_users']

    def unfollow_users(self, request, queryset):
        # Allow admin users to batch unfollow selected follow relationships
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully unfollowed {count} users.")
    unfollow_users.short_description = "Unfollow selected users"