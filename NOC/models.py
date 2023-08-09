from django.db import models

# Create your models here.
class MerakiDevice(models.Model):
    name = models.CharField(max_length=100)
    serial = models.CharField(max_length=100)
    mac = models.CharField(primary_key=True, max_length=24)
    publicIp = models.CharField(max_length=15)
    networkId = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    lastReportedAt = models.DateTimeField()
    model = models.CharField(max_length=100)
    tags = models.JSONField()
    wan1Ip = models.CharField(max_length=15, null=True, blank=True, default=None)
    wan1Gateway = models.CharField(max_length=15, null=True, blank=True, default=None)
    wan2Ip = models.CharField(max_length=15, null=True, blank=True, default=None)
    wan2Gateway = models.CharField(max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return self.serial

class UnifiSite(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    lan_health = models.CharField(max_length=100, null=True, blank=True, default="unknown")

    def __str__(self):
        return self.description
    
    
class UnifiDevice(models.Model):
    _id = models.CharField(max_length=255, primary_key=True)
    ip = models.CharField(max_length=255, null=True, blank=True)
    mac = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    connected_at = models.DateTimeField(default=None, null=True, blank=True)
    provisioned_at = models.DateTimeField(default=None, null=True, blank=True)
    mgmt_network_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    site_id = models.ForeignKey(UnifiSite, on_delete=models.CASCADE)
    state = models.IntegerField(null=True, blank=True)
    # last_uplink = models.JSONField(null=True, blank=True)
    # bec = models.ForeignKey(BEC, on_delete=models.CASCADE, null=True)
    gateway_mac = models.ForeignKey(MerakiDevice, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.mac
    

class Bec(models.Model):
    FW = models.CharField(max_length=100)
    IMEI = models.CharField(max_length=100)
    IMSI = models.CharField(max_length=100)
    ICCID = models.CharField(max_length=100)
    IP = models.CharField(max_length=100,null=True)
    LastConnect = models.CharField(max_length=100)
    MAC = models.CharField(max_length=100)
    MODEL = models.CharField(max_length=100,null=True)
    SYSUPTIME = models.CharField(max_length=100,null=True)
    Status = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    NETWORK = models.CharField(max_length=50,null=True)
    ENB_ID = models.CharField(max_length=50,null=True)
    CELLID = models.CharField(max_length=50,null=True)
    BAND = models.CharField(max_length=50)
    RSSI = models.IntegerField(null=True)
    SINR = models.IntegerField(null=True)
    unifi = models.ForeignKey(UnifiSite, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.MAC
    
class Kit(models.Model):
    meraki_device = models.OneToOneField(MerakiDevice, on_delete=models.CASCADE, null=True)
    unifi_device = models.ManyToManyField(UnifiDevice)
    site = models.OneToOneField(UnifiSite, on_delete=models.CASCADE)
    bec = models.ManyToManyField(Bec, blank=True)

    def __str__(self):
        return self.site.description