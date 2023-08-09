import requests
from NOC.models import UnifiDevice, MerakiDevice, UnifiSite
from django.utils import timezone
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from secretkeys import unifi_password

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




class PopulateUniFi():
    import time
    s = requests.Session()
    headers = {"Accept": "application/json","Content-Type": "application/json"}
    payload = {'username': 'inet-unifi', 'password': unifi_password}
    try:
        r = s.post('https://172.31.255.96:8443/api/login', headers = headers,  json = payload , verify = False, timeout = 4)
    except requests.exceptions.ReadTimeout as e:
        time.sleep(5)
        r = s.post('https://172.31.255.96:8443/api/login', headers = headers,  json = payload , verify = False, timeout = 4)
    sites = s.get('https://172.31.255.96:8443/api/self/sites', headers = headers, verify = False, timeout = 4).json()['data']
    sites = [site for site in sites if site.get('name') != 'default']
    count_of_sites = sum(1 for d in sites if 'desc' in d)

    def sitePopulater(self):
        UnifiSite.objects.all().delete()
        for site in self.sites:
            if site.get('name') != 'default':

                name = site['name']
                health = self.s.get(f'https://172.31.255.96:8443/api/s/{name}/stat/health' , headers = self.headers, verify = False, timeout = 4).json()['data']
                lan_health = [x['status'] for x in health if x['subsystem'] == 'lan'][0]
                sites = UnifiSite(
                    _id=str(site['_id']),
                    description=site['desc'].strip(),
                    name=site['name'],
                    lan_health=lan_health
                )
                sites.save()
        return self.count_of_sites
    def clients(self, vendor='Billion Electric Co. Ltd.'):
        from NOC.models import Bec
        bec_count = 0
        endpoints = ['/rest/user', '/stat/alluser', '/stat/sta']
        for site in self.sites:
            name = site['name']
            for r in endpoints:
                
                clients = self.s.get(f'https://172.31.255.96:8443/api/s/{name}{r}', headers = self.headers, verify = False, timeout = 5).json()['data']                
                for client in clients:
                    if client['oui'] == vendor:
                        # print(site['desc'], client['oui'], client['mac'])
                        bec_count += 1
                        mac = client['mac'].replace(':', '').upper()
                        try:
                            bec = Bec.objects.get(MAC=mac)
                            bec.unifi = UnifiSite(_id=site['_id'])
                            bec.save()
                        except Bec.DoesNotExist as e:
                            print(e, mac, site['desc']) # BEC is not in BECentral
                            continue

        return bec_count

    def devices(self):
        import concurrent.futures
        
        def fetch_device_data(site):
            
            '''Get the devices from each site'''
            def process_device(devices):
                '''Processes the devices into the model'''
                keys = ['_id','connected_at','gateway_mac','ip','mac','mgmt_network_id','model','name','provisioned_at','site_id','state','version','adopted']

                for device in devices:
                    device_data = {key: device.get(key) for key in keys}
                    connected_at = device_data.pop('connected_at')
                    connected_time = datetime.fromtimestamp(connected_at) if connected_at else None
                    last_reported_at = timezone.make_aware(connected_time) if connected_time else None

                    provisioned_at = device_data.pop('provisioned_at')
                    provisioned_time = datetime.fromtimestamp(provisioned_at) if provisioned_at else None
                    provisioned_at = timezone.make_aware(provisioned_time) if provisioned_time else None

                    site_id = device_data.pop('site_id')
                    gateway_mac = device_data.pop('gateway_mac')
                    if gateway_mac:
                        try:
                            mx = MerakiDevice.objects.get(mac=gateway_mac)
                        except MerakiDevice.DoesNotExist:
                            mx = None
                    else:
                        mx = None
                    
                    if device_data['adopted'] == True:
                        
                        site = UnifiSite.objects.get(_id=site_id)
                        device_data.pop('adopted')

                        device = UnifiDevice(
                            site_id=site,
                            gateway_mac=mx,
                            connected_at=last_reported_at,
                            provisioned_at=provisioned_at, 
                            **device_data)
                        device.save()                   
            
            url = f'https://172.31.255.96:8443/api/s/{site["name"]}/stat/device'
            response = self.s.get(url, verify=False).json()['data']
            process_device(response)
            
        UnifiDevice.objects.all().delete()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            device_data_all_sites = list(executor.map(fetch_device_data, self.sites))
            return len(device_data_all_sites)



