from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('shoping/', views.shop, name='shopping'),

    path('shoping/<str:slug>/', views.ProductDetail.as_view(), name='item-details'),
    path('profile/<str:slug>/orders', views.client_profile, name='user-profile'),
]
