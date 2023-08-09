import requests
from django.conf import settings

BASE_URL = "https://api.meraki.com/api/v1"

response = requests.get(BASE_URL+"/organizations", headers=settings.MERAKI_API_KEY, data = None)


INET_ORG    = [x['id'] for x in response.json() if x['name'] == "Infrastructure-Networks"][0]
PXD_ORG     = [x['id'] for x in response.json() if x['name'] == "Pioneer Drilling"][0]
# TEST_ORG    = [x['id'] for x in response.json() if x['name'] == "SD-WAN Testing"][0]
Precision    = [x['id'] for x in response.json() if x['name'] == "Precision"][0]

def orgs():
    response = requests.get(BASE_URL+"/organizations", headers=settings.MERAKI_API_KEY, data = None).json()
    return response

def devices(org):
    data = []
    response = requests.get(f"{BASE_URL}/organizations/{org}/devices/statuses", headers=settings.MERAKI_API_KEY, data = None).json()
    return response