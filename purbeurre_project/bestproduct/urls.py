from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.listing),
    url(r'^(?P<user_id>[0-9]+)/$', views.detail),
    url(r'^search/$', views.search),
]