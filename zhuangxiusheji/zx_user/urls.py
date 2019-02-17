from . import views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index_for_user/$', views.index_for_user, name='index_for_user'),
    url(r'^index_for_company/$', views.index_for_comapny, name='index_for_company'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^login/$', views.login, name='login'),
    url(r'^select/$', views.select_kind, name='select'),
    url(r'^kind_handel/$', views.kind_handel, name='kind_handel'),
    url(r'^register/$', views.register, name='register'),
    url(r'^longin_handel/$', views.login_handel, name='longin_handel'),
    url(r'^register_handel_forOrd/$', views.register_handel_forOrd, name='register_handel_forOrd'),
    url(r'^register_handel_forCom/$', views.register_handel_forCom, name='register_handel_forCom'),
    url(r'^del_session/$', views.del_session, name='del_session'),
    url(r'^verifycode$', views.verifycode, name='verifycode'),
    url(r'^aboutUs/$', views.aboutUs, name='aboutUs'),
]