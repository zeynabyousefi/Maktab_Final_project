from django.urls import path

from .views import *

urlpatterns = [
    path('email-view/', EmailView.as_view(), name='email_view'),

]
