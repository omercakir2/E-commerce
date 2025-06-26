from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_pro_view,name='add_pro'),
    path('remove/',views.remove_pro_view,name='remove_pro'),
    path('list/',views.list_pro_view,name='list_pro'),
    path('products/remove/<int:pk>/', views.remove_product_view, name='remove_product'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('add_stock/<int:pk>/', views.add_stock_view, name='add_stock'),
    path('remove_stock/<int:pk>/', views.remove_stock_view, name='remove_stock'),
]
