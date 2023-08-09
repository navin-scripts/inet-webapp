# tasks.py

from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from .models import MerakiDevice
from .conf import INET_ORG, Precision
import requests

@shared_task
def update_meraki_devices():
    # Make an API request to retrieve Cisco Meraki data
    orgs = [INET_ORG, Precision]
    for org in orgs:
        url = f"https://api.meraki.com/api/v1/organizations/{org}/devices/statuses"

        response = requests.get(url, headers=settings.MERAKI_API_KEY)
        if response.status_code == 200:
            devices_data = response.json()

            # Loop through the devices data and update MerakiDevice instances
            for device_data in devices_data:
                name = device_data.get('name')
                serial_number = device_data.get('serial')
                mac_address = device_data.get('mac')
                public_ip = device_data.get('publicIp')
                network_id = device_data.get('networkId')
                status = device_data.get('status')
                last_reported_at_str = device_data.get('lastReportedAt')
                last_reported_at = datetime.strptime(last_reported_at_str, '%Y-%m-%dT%H:%M:%S.%fZ') if last_reported_at_str else None
                last_reported_at = timezone.make_aware(last_reported_at) if last_reported_at else None
                product_type = device_data.get('productType')
                components = device_data.get('components')
                model = device_data.get('model')
                tags = device_data.get('tags')
                using_cellular_failover = device_data.get('usingCellularFailover')
                wan1_ip = device_data.get('wan1Ip')
                wan1_gateway = device_data.get('wan1Gateway')
                wan1_ip_type = device_data.get('wan1IpType')
                wan1_primary_dns = device_data.get('wan1PrimaryDns')
                wan1_secondary_dns = device_data.get('wan1SecondaryDns')
                wan2_ip = device_data.get('wan2Ip')


                # Create or update MerakiDevice instance
                MerakiDevice.objects.update_or_create(
                    serial_number=serial_number,
                    defaults={
                        'name': name,
                        'mac_address': mac_address,
                        'public_ip': public_ip,
                        'network_id': network_id,
                        'status': status,
                        'last_reported_at': last_reported_at,
                        'product_type': product_type,
                        'components': components,
                        'model': model,
                        'tags': tags,
                        'using_cellular_failover': using_cellular_failover,
                        'wan1_ip': wan1_ip,
                        'wan1_gateway': wan1_gateway,
                        'wan1_ip_type': wan1_ip_type,
                        'wan1_primary_dns': wan1_primary_dns,
                        'wan1_secondary_dns': wan1_secondary_dns,
                        'wan2_ip': wan2_ip
                    }
                )
        else:
            print("Failed to retrieve Meraki device data.")

