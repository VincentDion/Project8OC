from django.urls import path

from . import views

app_name = "bestproduct"

urlpatterns = [
    path('', views.index, name='index'),
    path('replace/', views.replace, name='replace'),
    path('detail/<str:product_id>/', views.detail, name='detail'),
]

"""
urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)/$', views.detail),
    url(r'^replace/$', views.replace),
]
"""