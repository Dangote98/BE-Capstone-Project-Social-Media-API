from django.contrib import admin
from .models import Post, Follow, Profile
from django.core.exceptions import ValidationError

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('content',)

    # Override save_model to add logic for updating posts
    def save_model(self, request, obj, form, change):
        # Check if this is an update (and not a new creation)
        if change:
            # Optional: Add any restrictions here, like ensuring only the post's owner can update
            if obj.user != request.user:
                raise ValidationError("You can only update your own posts.")

        super().save_model(request, obj, form, change)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')

    def save_model(self, request, obj, form, change):
        if obj.follower == obj.following:
            raise ValidationError("Users cannot follow themselves.")
        super().save_model(request, obj, form, change)

    actions = ['unfollow_users']

    def unfollow_users(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully unfollowed {count} users.")
    unfollow_users.short_description = "Unfollow selected users"
