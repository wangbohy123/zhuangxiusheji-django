from . import views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^showCompanies/$', views.show_company, name='showCompanies'),
    url(r'^show_detail/$', views.show_detail, name='show_detail'),
    url(r'^give_case/$', views.give_case, name='give_case'),
    url(r'^case_handel$', views.case_handel, name='case_handel'),
    url(r'^check_case/$', views.check_case, name='check_case'),
    url(r'^user_case/$', views.user_case, name='user_case'),
    url(r'^company_case/$', views.company_case, name='company_case'),
    url(r'^company_suggestion/$', views.company_suggestion, name='company_suggestion'),
    url(r'^suggestion_handel/$', views.suggestion_handel, name='suggestion_handel'),
    url(r'^write_comment/$', views.write_comment, name='write_comment'),
    url(r'^comment_handel/$', views.comment_handel, name='comment_handel'),
]