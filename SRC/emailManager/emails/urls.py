from django.urls import path

from .views import *

urlpatterns = [
    path('email-view/', EmailInboxView.as_view(), name='email_view'),
    # path('new-email/', NewEmail.as_view(), name='new_email'),
    path('new-email/', AddNewEmail.as_view(), name='new_email'),
    path('#sentbox/', EmailSentboxView.as_view(), name='email_sentbox'),
    path('#drafts/', EmailDraftsView.as_view(), name='email_drafts'),
    path('detail/<int:email_id>/', DetailEmailView.as_view(), name='detail_email'),
    # path('reply/<int:email_id>/', EmailReply.as_view(), name='email_reply'),
    path('add-label/', AddLabelView.as_view(), name='add_label'),

]
