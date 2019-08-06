from django.conf.urls import url

from . import views

urlpatterns = [
#     url(r'^$', views.listing),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail),
    url(r'^replace/$', views.replace),
]