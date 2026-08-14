"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path


def spa_view(request):
    """Serves the built React app's index.html for client-side routes."""
    index_path = Path(settings.WHITENOISE_ROOT) / 'index.html'
    if index_path.exists():
        return HttpResponse(index_path.read_text(encoding='utf-8'), content_type='text/html')
    return HttpResponse('Frontend not built. Run `npm run build` in the frontend directory.', status=503)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Jwt login endpoints for users
    path('api/clinics/', include('clinics.urls')),  # Clinic management endpoints
    path('api/mothers/', include('mothers.urls')),  # Mother management endpoints
    path('api/appointments/', include('appointments.urls')),  # Follow-up appointment endpoints
    path('api/tips/', include('tips.urls')),
    path('api/chat/', include('chat.urls')),
    re_path(r'^(?!api/|admin/|static/|assets/).*$', spa_view, name='spa'),
]
