from . import views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^show/$', views.user_center, name='show'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^modify_personal$', views.modify_personal, name='modify_personal'),
    url(r'^modify_personal_handel$', views.modify_personal_handel, name='modify_personal_handel'),
    url(r'^show_for_company/$', views.user_center_company, name='show_for_company'),
    url(r'^corporate/$', views.corporate, name='corporate'),
    url(r'^modify_company/$', views.modify_company, name='modify_company'),
    url(r'^modify_company_handel/$', views.modify_company_handel, name='modify_company_handel')
]