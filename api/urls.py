from django.urls import path
from .views import *

urlpatterns = [
    path('user-id/', UserIDView.as_view(), name='user-id'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<pk>/', ProductDetailView.as_view(), name='product-detail'),

]
