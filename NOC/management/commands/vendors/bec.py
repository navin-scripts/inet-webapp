from NOC.models import Bec
import requests
from secretkeys import becheaders, becpayload

def becentral():
    import json
    loginUrl = 'https://api.becentral.io:5580/api/lcmsUsers/signin'
    url = 'https://api.becentral.io:5580/api/deviceLists'
    
    headers = becheaders
    payload = becpayload
    
    s = requests.Session()
    login = s.post(url=loginUrl, headers=headers, json=payload).json()
    deviceList = s.get(url, headers=headers).json()
    becs = 0
    for bec in deviceList:
        if 'MAC' in bec:
            becs += 1
        radio = Bec(
            FW=bec['FW'],
            IMEI=bec['IMEI'],
            IMSI=bec['IMSI'],
            ICCID=bec['ICCID'],
            IP=bec['IP'],
            MAC=bec['MAC'],
            MODEL=bec['MODEL'],
            name=bec['name'],
            owner=bec['owner'],
            NETWORK=bec['NETWORK'],
            ENB_ID=bec['ENB_ID'],
            CELLID=bec['CELLID'],
            BAND=bec['BAND'],
            RSSI=bec['RSSI'],
            SINR=bec['SINR'],
            LastConnect=bec['LastConnect'],
            Status=bec['Status'],
            SYSUPTIME=bec['SYSUPTIME'],
            id=bec['id']
        )
        radio.save()
    return becs