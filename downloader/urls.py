"""
URL configuration for downloader project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),path("fbdownloader" , include('apiview.urls')),
    path("twdownloader" , include('apitwitterapp.urls')),
    path("ttdownloader" , include('tiktok.urls')),
    path("instadownloader" , include('instagram.urls')),
    path("aiodownloader" , include('aio.urls')),
    path("dailydownloader" , include('dailymotion.urls')),
    path("thdownloader" , include('threadappinsta.urls')),
    path("likeedownloader" , include('likee.urls')),
    path("snackdownloader" , include('snackvideo.urls')),
    path("linkedindownloader" , include('linkedin.urls')),
    path("pinterestdownloader" , include('pinterestvideo.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]
