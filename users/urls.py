from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('display/',views.display_users_view,name='display'),
    path('logout/',views.logout_view,name='logout')
]
