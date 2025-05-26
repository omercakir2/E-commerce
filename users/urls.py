from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('display/',views.display_users_view,name='display'),
    path('logout/',views.logout_view,name='logout'),
    path('verify-2fa/', views.verify_2fa_view, name='verify_2fa'),
    
    
    path('reset-password/', views.custom_password_reset_request, name='custom_password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
    path('reset-password-done/', views.password_reset_done, name='password_reset_done'),
    path('reset-password-complete/', views.password_reset_complete, name='password_reset_complete'),
    
    
    #last
    path('<str:user_mail>/', views.user_detail_by_email, name='user_detail_by_email'),
]
