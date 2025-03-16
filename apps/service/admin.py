from django.contrib import admin

from apps.service.models import *

# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(ServiceReservedDate)
