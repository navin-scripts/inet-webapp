from NOC.models import MerakiDevice
from scripts.meraki.conf import INET_ORG, PXD_ORG, Precision, devices

def populateMerakis():
    MerakiDevice.objects.all().delete()
    merged_lists = []
    orgs = [INET_ORG, PXD_ORG, Precision]
    for x in orgs:
        merged_lists.append(devices(x))
        
    count_of_merakis = 0
    for p in merged_lists: 
        for i in p:
            count_of_merakis += 1
            meraki = MerakiDevice(
                name = i.get('name'),
                serial = i.get('serial'),
                mac = i.get('mac'),
                publicIp = i.get('publicIp'),
                networkId = i.get('networkId'),
                status =i.get('status'),
                lastReportedAt = i.get('lastReportedAt'),
                model = i.get('model'),
                tags = i.get('tags'),
                wan1Ip = i.get('wan1Ip'),
                wan1Gateway = i.get('wan1Gateway'),
                wan2Ip = i.get('wan2Ip'),
                wan2Gateway = i.get('wan2Gateway'),
            )
            meraki.save()
    return count_of_merakis