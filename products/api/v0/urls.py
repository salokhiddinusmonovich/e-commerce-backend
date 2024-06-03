from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductByCategoryListAPIView.as_view(), name='product_by_category')
]