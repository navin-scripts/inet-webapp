from django.db import models

class TunnelInterface(models.Model):
    site_name = models.CharField(max_length=100,null=True, blank=True)
    interface = models.CharField(primary_key=True, null=False, max_length=100)
    tunnel_peer_ip = models.CharField(null=True, blank=True,max_length=15)
    tunnel_ip = models.CharField(null=True, blank=True,max_length=15)
    tunnel_mask = models.CharField(null=True, blank=True,max_length=15)
    remote_gateway = models.CharField(null=True, blank=True,max_length=15)
    subscription_ip = models.CharField(null=True, blank=True,max_length=15)

    def __str__(self):
        return self.site_name

class TunnelRoute(models.Model):
    interface = models.ForeignKey(TunnelInterface, on_delete=models.CASCADE)
    gateway_ip = models.CharField(null=True, blank=True,max_length=15)
    destination = models.CharField(null=True, blank=True,max_length=15)
    mask = models.CharField(null=True, blank=True,max_length=15)
    vrf = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self) -> str:
        return self.destination