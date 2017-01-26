"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.static import serve
from django.conf.urls.static import static
from imagersite import views, settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_page, name="home"),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^user/', include('imager_profile.urls')),
    url(r'^images/', include('imager_images.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [
    #     url(r'^media/(?P<path>.*)$', serve,
    #     {'document.root': settings.MEDIA_ROOT}),
    # ]
