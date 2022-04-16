from django.urls import path
from .views import *
from .api import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('', Index.as_view(), name='home'),
    path('reset-password', ResetPassword.as_view(), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', reset_password_confirm, name='reset_password_confirm'),
    path('reset-password-confirm/', UserResetPasswordVerifyCodeView.as_view(), name='reset_password_confirm_phone'),
    path('reset-password-confirm-complete/', ResetPasswordConfirmByPhone.as_view(),
         name='reset_password_confirm_phone_complete'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('add-contact/<int:user_id>/', UserContactView.as_view(), name='add_contact'),
    path('add-contact/', UserContactView.as_view(), name='add_contact'),
    path('all-users/', ShowAllContact.as_view(), name="all_contacts"),
    path('detail-contact/<int:contact_id>/', DetailContactView.as_view(), name="detail_contact"),
    path('edit/<int:contact_id>', Update.as_view(), name="contact_update"),
    path('delete/<int:contact_id>/', ContactDelete.as_view(), name="contact_delete"),
    path('export-contact/', export_contact_csv, name="export_contact"),
    path('search-contact/', SearchContacts.as_view(), name="search_contact"),
    path('add-signature/', AddSignature.as_view(), name="add_signature"),
    path('api-contact/', detail_contact, name="api_contact"),
    path('api-email/', detail_email, name="api_email"),
    path('search-contacts/', csrf_exempt(search_contacts), name="search_contacts"),
]
