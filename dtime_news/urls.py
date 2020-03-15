"""dtime_news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from rest_framework import routers, serializers

router = routers.DefaultRouter()

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/user-auth/', include('user_auth.urls')),
    url(r'^api/user-profile/', include('user_profile.urls')),
    url(r'^api/news/', include('news.urls')),
    url(r'^api/file-manager/', include('file_manager.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)