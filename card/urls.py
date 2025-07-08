from django.urls import path
from . import views

urlpatterns = [
    path('',views.see_card,name='see_card'),
    path('add_to_card/<int:pk>/',views.add_to_card,name='add_to_card'),
]
