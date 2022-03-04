from django.contrib import admin
from .models import *

admin.site.register(Email)
admin.site.register(EmailPlaceHolders)
admin.site.register(UserEmailMapped)