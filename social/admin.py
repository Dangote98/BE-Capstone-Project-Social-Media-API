from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Post, Follow, Profile
from django.core.exceptions import ValidationError

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

# Custom logout view function
def logout_view(request):
    logout(request)
    return redirect('/admin/login/')  # Redirect to admin login page after logout

# Added the custom URL for logout directly to the admin site URLs
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('logout/', self.admin_view(logout_view), name='admin_logout'),
        ]
        return custom_urls + urls

# Replaced the default admin site with the custom one
admin_site = CustomAdminSite(name='custom_admin')

# Registered my models with the custom admin site
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Post, PostAdmin)
admin_site.register(Follow, FollowAdmin)
