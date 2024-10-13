from django.apps import AppConfig

class SocialConfig(AppConfig):
    """Configuration for the Social app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social'

    def ready(self):
        """Import signals to register them when the app is ready."""
        import social.signals  # Ensure that your signals are loaded
