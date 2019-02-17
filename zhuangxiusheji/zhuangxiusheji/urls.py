"""zhuangxiusheji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from zx_user.views import index
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('zx_user.urls',namespace='user')),
    url(r'^user_center/', include('zx_user_center.urls', namespace='user_center')),
    url(r'^anli/', include('zx_anli.urls', namespace='anli')),
    url(r'^draw/', include('zx_draw.urls', namespace='draw')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
