from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model for user posts
class Post(models.Model):
    content = models.TextField()  # The text content of the post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the post
    timestamp = models.DateTimeField(auto_now_add=True)  # Time the post was created
    media = models.URLField(blank=True, null=True)  # Optional field for media (image/video) URLs
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, blank=True, null=True)  # Type of media (optional)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"  # Returns a string representation of the post


# Model for managing following relationships between users
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)  # User who follows another user
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)  # User being followed

    class Meta:
        unique_together = ('follower', 'following')  # Ensures a user can only follow another user once
        indexes = [
            models.Index(fields=['follower']),  # Index to optimize querying by follower
            models.Index(fields=['following']),  # Index to optimize querying by following
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"  # Returns a string representation of the follow relationship


# Model for user profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    bio = models.TextField(blank=True, null=True)  # Optional bio field
    profile_picture = models.URLField(blank=True, null=True)  # Optional field for the profile picture URL

    def __str__(self):
        return f"{self.user.username}'s Profile"  # Returns a string representation of the profile


# Signal to automatically create or update a user's profile when the user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Create profile when a new user is created
    instance.profile.save()  # Save the profile every time the user is saved
