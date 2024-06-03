from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', sign_up, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/', profile_view, name='profile'),
    path('profile-edit/', profile_edit_view, name='profile_edit'),
    path('profile-delete/', profile_delete_view, name='profile_delete'),
]