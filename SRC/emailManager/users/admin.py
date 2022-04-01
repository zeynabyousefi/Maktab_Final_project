import os

from django.contrib import admin
from django.shortcuts import render

from .models import *

import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.http import JsonResponse
from django.urls import path
from datetime import timedelta, datetime
from .models import *
from emails.models import *

# admin.site.register(CustomUser)
admin.site.register(OtpCode)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("owner_contact", "name",)  # display these table columns in the list view
    ordering = ("-time",)
    date_hierarchy = "time"

    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

        # JSON endpoint for generating chart data that is used for dynamic loading
        # via JS.

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            Contact.objects.annotate(date=TruncMonth("time"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )


def sizify(value, *args):
    """
    Simple kb/mb/gb size:
    """
    # value = ing(value)
    if int(value) < 512000:
        value = int(value) / 1024.0
        ext = 'kb'
    elif int(value) < 4194304000:
        value = int(value) / 1048576.0
        ext = 'mb'
    else:
        value = int(value) / 1073741824.0
        ext = 'gb'
    return '%s %s' % (str(round(int(value), 2)), ext)


@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "send_emails", "received_emails", "is_active", "is_staff", "size_of_upload_file")
    readonly_fields = ("send_emails", "received_emails", "is_active", "is_staff", "size_of_upload_file")
    # display these table columns in the list view
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    def is_active(self, obj):
        active = CustomUser.objects.filter(is_active=True, username=obj)
        return active

    def is_staff(self, obj):
        staff = CustomUser.objects.filter(is_active=True, username=obj)
        return staff

    def send_emails(self, obj):
        result = Email.objects.filter(author=obj).count()
        return result

    def received_emails(self, obj):
        inbox = EmailPlaceHolders.objects.get(place_holder="inbox")
        result = UserEmailMapped.objects.filter(user=obj, place_holder=inbox).count()
        return result

    def size_of_upload_file(self, obj):
        user_files = Email.objects.filter(author=obj).exclude(attachment__isnull=False, attachment=None)
        total = sum(int(objects.attachment_size) for objects in user_files if objects.attachment_size)
        size = sizify(total)
        print("{" * 90)
        print(total)
        return total

    def changelist_view(self, request, extra_context=None):
        email_file = Email.objects.filter(attachment__isnull=False).exclude(attachment='')
        usernames = []
        file_data = []
        for email in email_file:
            usernames.append(CustomUser.objects.get(pk=email.author.id))
            usernames = set(usernames)
            usernames = list(usernames)
        for user in set(usernames):
            files_user = email_file.filter(author=user)
            total = sum(int(objects.attachment_size) for objects in files_user if objects.attachment_size)
            self.size_of_upload_file(total)
            file_data.append({"user": user.username, "user_size": total})
            print(file_data)
            print(")" * 90)
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        # as_json1 = json.dumps(list(file_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json, "file_data": file_data}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

        # JSON endpoint for generating chart data that is used for dynamic loading
        # via JS.

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            CustomUser.objects.annotate(date=TruncMonth("date_joined"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )
