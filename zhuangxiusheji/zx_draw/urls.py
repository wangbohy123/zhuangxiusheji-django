from . import views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^image/$', views.loadImage, name='image'),
    url(r'^upload_image/', views.upload_image, name='upload_image'),
]