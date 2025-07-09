from django.urls import path
from . import views

urlpatterns = [
    path('',views.see_card,name='see_card'),
    path('add_to_card/<int:pk>/',views.add_to_card,name='add_to_card'),
    path('remove_from_card/<int:productid>/<int:userid>/',views.remove_from_card,name='remove_from_card'),
    path('clear_card/',views.clear_card,name='clear_card')
]
