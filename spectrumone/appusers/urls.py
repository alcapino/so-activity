from django.conf.urls import url
from appusers import views

urlpatterns = [
    url(r'^accesstoken/(?P<pk>[0-9]+)/$', views.access_token),
    url(r'^users/$', views.user_list),
    url(r'^user/$', views.user_registration),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^user/(?P<pk>[0-9]+)/(?P<t>[\w]+)$', views.user_detail),
]