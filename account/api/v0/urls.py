from django.urls import path

from account.api.v0.views import SignUp, UserUpdateAPIView, UserChangePasswordView

urlpatterns = [
    path('register/', SignUp.as_view(), name='register'),
    path('update/', UserUpdateAPIView.as_view(), name='update_profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]