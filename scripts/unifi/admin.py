# from django.contrib import admin
# from .models import Site, Device, BEC
# from scripts.meraki.models import MerakiDevice
# from django.contrib import admin
# from .models import Location


# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ('site', 'get_device_count', 'get_bec_count', 'get_bec_ids', 'get_devices')
#     search_fields = ('site', 'get_device_count', 'get_bec_count', 'get_bec_ids', 'get_devices')
#     def has_change_permission(self, request, obj=None):
#         return False
#     # list_display = ('site', 'get_device_count', 'get_bec_count', 'get_meraki_status')

#     def get_devices(self,obj):
#         devs = obj.devices.values_list('mac', flat=True)
#         devices = [d for d in devs]
#         return ', '.join(devices)

#     def get_device_count(self, obj):
#         return obj.devices.count()

#     def get_bec_count(self, obj):
#         return obj.bec.count()
    
#     def get_bec_ids(self, obj):
#         bec_ids = obj.bec.values_list('_id', flat=True)
#         return ', '.join(bec_ids)

#     get_device_count.short_description = 'Device Count'
#     get_bec_count.short_description = 'BEC Count'
#     get_bec_ids.short_description = 'BEC MACs'
#     # get_meraki_device_serial_number.short_description = 'Meraki Serials'
#     get_devices.short_description = 'Devices'


# admin.site.site_header = 'Location Admin'
# admin.site.site_title = 'Location Admin Panel'
# admin.site.index_title = 'Welcome to the Location Admin Panel'


# class MerakisInline(admin.TabularInline):
#     model = MerakiDevice

# class DevicesInline(admin.TabularInline):
#     model = Device


# @admin.register(Site)
# class SiteAdmin(admin.ModelAdmin):
#     list_display = ('description', 'name')
#     search_fields = ('description', 'name')
#     def getDevices(self, obj):
#         devices = obj.Device_set.all()
#         return ", ".join(device for device in devices)
#     getDevices.short_description = "Devices"
#     inlines = [DevicesInline]
    


# @admin.register(Device)
# class UniFiDeviceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'mac')
#     search_fields = ('name', 'mac', 'model')
#     # def getMerakis(self, obj):
#     #     merakis = obj.Device_set.all()
#     #     return ", ".join(device for device in merakis)
#     # getMerakis.short_description = "Merakis"
#     # inlines = [MerakisInline]



# admin.site.site_header = 'UniFi Device Admin'
# admin.site.site_title = 'UniFi Device Admin'