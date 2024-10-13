from django.contrib import admin
from django.urls import path, include
from social.views import home_redirect  # Import home_redirect function for root access redirection

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel access
    path('', home_redirect, name='home_redirect'),  # Redirect root URL based on authentication
    path('api/', include('social.urls')),  # Include 'social' app URLs (API, login, signup, etc.)
]
