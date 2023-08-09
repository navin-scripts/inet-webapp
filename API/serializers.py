from rest_framework import serializers
from NOC.models import UnifiSite, Kit, UnifiDevice, Bec

class UnifiSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnifiSite
        fields = ('description', 'name')

class UnifiDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnifiDevice
        fields = ('mac', 'model')

class BecDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bec
        fields = ('MAC', 'IP', 'ICCID')

class KitSerializer(serializers.ModelSerializer):
    site_description = serializers.CharField(source='site.description', read_only=True)
    meraki = serializers.CharField(source='meraki_device.serial', read_only=True)
    unifi_device_macs = serializers.SerializerMethodField()  # Custom field for unifi_device macs
    becs = serializers.SerializerMethodField()

    class Meta:
        model = Kit
        fields = ('site_description', 'meraki', 'unifi_device_macs', 'becs')
    
    def get_unifi_device_macs(self, obj):
        return UnifiDeviceSerializer(obj.unifi_device.all(), many=True).data
    def get_becs(self, obj):
        return BecDeviceSerializer(obj.bec.all(), many=True).data
