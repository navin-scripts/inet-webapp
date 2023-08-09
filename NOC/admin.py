from django.contrib import admin
from .models import Kit, Bec, MerakiDevice, UnifiDevice, UnifiSite

class KitAdmin(admin.ModelAdmin):
    list_display = ['site', 'get_unifi_devices', 'get_becs', 'meraki_device', 'get_lan_statuses']
    search_fields = ['site__description', 'site__lan_health']

    def get_lan_statuses(self, obj):
        if obj.site:
            return obj.site.lan_health
        return None
    get_lan_statuses.short_description = 'UniFi LAN status' 

    def get_unifi_devices(self, obj):
        return ', '.join([device.mac for device in obj.unifi_device.all()])
    get_unifi_devices.short_description = 'UniFi Devices'

    def get_becs(self, obj):
        return ', '.join([bec.IP for bec in obj.bec.all()])
    get_becs.short_description = 'BECs'

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Kit, KitAdmin)


@admin.register(Bec)
class BecAdmin(admin.ModelAdmin):
    list_display = ['IP', 'name', 'Status', 'MAC']
    search_fields = ('name', 'IP', 'Status', 'MAC')
    def has_change_permission(self, request, obj=None):
        return False
    
@admin.register(MerakiDevice)
class MerakiDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial', 'networkId', 'status']
    search_fields = ('name', 'serial', 'networkId', 'status')
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(UnifiDevice)
class UnifiDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'mac', 'state', 'ip']
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(UnifiSite)
class UnifiSiteAdmin(admin.ModelAdmin):
    list_display = ['description', 'name', 'lan_health']
    search_fields = ('description', 'name', 'lan_health')
    def has_change_permission(self, request, obj=None):
        return False