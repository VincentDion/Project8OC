from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from django.urls import path

from bestproduct import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bestproduct.urls', namespace='besproduct')),
]
