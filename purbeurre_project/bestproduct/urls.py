from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "bestproduct"

urlpatterns = [
    path('', views.index, name='index'),
    path('replace/', views.replace, name='replace'),
    path('detail/<str:product_id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('favorite/', views.favorite, name='favorite'),
    path('login/', auth_views.LoginView.as_view(
         template_name='bestproduct/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(
         template_name='bestproduct/logout.html'),
         name='logout'),
    path('add_favorite/<str:product_id>/', views.add_favorite,
         name='add_favorite'),
    path('legal_notice/', views.legal_notice, name='legal_notice'),
]
