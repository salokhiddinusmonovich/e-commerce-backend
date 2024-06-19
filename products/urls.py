from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name='home'),
    path('products/<int:pk>', product_detail, name='product_detail'),
    path('store/', store, name='store'),
    path('category/<int:pk>/', get_category, name='category'),

]
