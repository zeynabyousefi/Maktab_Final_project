from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('', Index.as_view(), name='home'),
    path('reset-password', ResetPassword.as_view(), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', reset_password_confirm, name='reset_password_confirm'),
    path('reset-password-confirm/', UserResetPasswordVerifyCodeView.as_view(), name='reset_password_confirm_phone'),
    path('reset-password-confirm-complete/', ResetPasswordConfirmByPhone.as_view(), name='reset_password_confirm_phone_complete'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),

]
