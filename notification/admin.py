from django.contrib import admin
from .models import DeviceToken, CertFile


class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_token', 'device_type', 'user')
    list_display_links = ('id', 'device_token', 'device_type', 'user')

admin.site.register(DeviceToken, DeviceTokenAdmin)
