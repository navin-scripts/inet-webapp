
def populateKits():
    from NOC.models import Kit, MerakiDevice, UnifiSite, UnifiDevice, Bec
    from django.db.utils import IntegrityError
    Kit.objects.all().delete()
    unifi_sites = UnifiSite.objects.all()
    kits = 0
    for site in unifi_sites:
        kit = Kit.objects.create(site=site)
        devices = UnifiDevice.objects.filter(site_id=site._id)
        gateway_macs = devices.values_list('gateway_mac', flat=True)
        becs = Bec.objects.filter(unifi=site._id)
        kit.unifi_device.set(devices)
        kit.bec.set(becs)
        kit.save()
        kits += 1
        for x in set(gateway_macs):
            if x:
                meraki = MerakiDevice.objects.filter(mac=x).first()
                try:
                    kit.meraki_device = meraki
                    kit.save()
                except IntegrityError as e:
                    print("Skipped because of IntegrityError in meraki loop: ", "-" * 10, meraki) 
    return kits