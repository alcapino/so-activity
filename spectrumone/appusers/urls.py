from django.conf.urls import url
from appusers import views

urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^user/$', views.user_registration),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail),
]