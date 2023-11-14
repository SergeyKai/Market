from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('change_data/', views.user_change_data, name='change_data'),
    path('change_password/',
         PasswordChangeView.as_view(template_name='user/user_change_password.html'),
         name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),

]
