import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.http import JsonResponse
from django.urls import path

from .models import *

# admin.site.register(Email)
admin.site.register(EmailPlaceHolders)
admin.site.register(UserEmailMapped)
admin.site.register(EmailReceiver)
admin.site.register(Filter)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "subject", "created_date",)  # display these table columns in the list view
    ordering = ("-created_date",)
    date_hierarchy = "created_date"

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
            Email.objects.annotate(date=TruncMonth("created_date"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )


    # fields = readonly_fields

    # list_filter = ("username",)

