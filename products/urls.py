from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_pro_view,name='add_pro'),
    path('remove/',views.remove_pro_view,name='remove_pro'),
    path('list/',views.list_pro_view,name='list_pro'),
]
