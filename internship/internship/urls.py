from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include('app.urls', namespace='app')),  # Use a unique namespace for app
    path("admin/", admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('chat/', include('chatbot.urls', namespace='chatbot')),  # Use a unique namespace for chatbot
    path("dash/", include('app.urls', namespace='app_dash')),
  # Make sure this URL has a unique name or remove it if it's a duplicate
    path('', include('app1.urls',namespace='app1')),
    
]

# Add the following lines to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


"""internship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


