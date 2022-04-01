from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *
from emails.models import *


@api_view()
@permission_classes([IsAuthenticated, ])
def detail_contact(request):
    contact = Contact.objects.filter(owner_contact=request.user)
    ser_data = ContactUserSerializer(contact, many=True)
    return Response(ser_data.data)


@api_view()
@permission_classes([IsAuthenticated, ])
def detail_email(request):
    email = Email.objects.filter(author=request.user)
    ser_data = EmailSerializer(email, many=True)
    return Response(ser_data.data)
