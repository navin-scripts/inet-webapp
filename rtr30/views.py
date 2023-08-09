from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from anadarko.models import TunnelInterfaces, TunnelRoutes
from anadarko.configupdate import configRequest
import ipaddress, os
from django.conf import settings
import xml.etree.ElementTree as ET


base_dir = settings.BASE_DIR

def generate_config(SITENAME, network, tunnel_ip, tunnel_peer_ip):
# Load the configuration file
    tree = ET.parse('base.cfg')
    root = tree.getroot()

    LAN_GATEWAY = str(network.network_address + 1)
    LAN_START = str(network.network_address + 2)
    LAN_SUBNET_MASK = str(network.netmask)

    # LAN CONFIGURATION
    lan = root.find('Lan/Entry0')
    lan.set('IP', LAN_GATEWAY)
    lan.set('netmask', LAN_SUBNET_MASK)

    # DHCP configuration
    dhcp = root.find('Dhcpd/Option60')
    dhcp.set('subnetMask', LAN_SUBNET_MASK)
    dhcp.set('router', LAN_GATEWAY)

    dhcp_start = root.find('Dhcpd/Common')
    dhcp_start.set('start', LAN_START)
    dhcp_start.set('router', LAN_GATEWAY)

    # GRE CONFIGURATION
    gre = root.find('Gre/Entry0')
    gre.set('remotegw', '172.17.254.46')
    gre.set('tunnelip', tunnel_peer_ip)
    gre.set('peerip', tunnel_ip)

    # WRITE CONFIGURATION
    tree.write(str(SITENAME)+'.cfg')
    return str(SITENAME)+'.cfg'


def configRequest(SITENAME, network, tunnel_ip, tunnel_peer_ip):
    from django.http import FileResponse
    from django.utils.text import slugify
    
    # Process the form submission and generate the file
    SITENAME = slugify(SITENAME)
    # filename = slugify(SITENAME) + '.cfg'
    filename = generate_config(SITENAME, network, tunnel_ip, tunnel_peer_ip)
    current_directory = os.getcwd()

    # Create a FileResponse object with the file
    response = FileResponse(open(filename, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def search_interfaces(request):
    term = request.GET.get('term', '')  # Get the search term from the request
    try:
        interfaces = TunnelInterfaces.objects.filter(site_name__contains=term).values_list('interface', 'site_name', 'subscription_ip')
        results = [{'id': interface, 'text': site_name + ' LTE IP: ' + subscription_ip} for interface, site_name, subscription_ip in interfaces]
    except:
        interfaces = TunnelInterfaces.objects.filter(site_name__contains=term).values_list('interface', 'site_name')
        results = [{'id': interface, 'text': site_name} for interface, site_name in interfaces]
    if results: return JsonResponse(results, safe=False)
    else: return JsonResponse([{'id': "error", 'text': "No Results Found"}], safe=False)



def greForm(request):
    interfaces = TunnelInterfaces.objects.all()
    context = {"interfaces":interfaces}
    return render(request, 'index.html', context)

def confGenerator(request):
    from django.http import HttpResponse, JsonResponse
    config_file_data = {}
    # if request.method == 'POST':
        # Assuming TunnelRoutes has a ForeignKey or OneToOneField named 'interface' related to TunnelInterfaces
    interface_value = request.POST.get('interface')

    # Retrieve TunnelRoutes objects related to the specified interface
    routes_data = TunnelRoutes.objects.filter(interface__interface=interface_value)
    intefaces = TunnelInterfaces.objects.all()

    # Access fields for TunnelRoutes objects
    routes_fields = [{key: value for key, value in route.__dict__.items() if not key.startswith('_')} for route in routes_data]

    # Access related TunnelInterfaces fields
    interfaces_data = [route.interface.__dict__ for route in routes_data]

    joined_data = []
    siteName = {}

    for route_field, interface_data in zip(routes_fields, interfaces_data):
        route_field.pop('_state', None)
        interface_data.pop('_state', None)
        joined_data.append({**route_field, **interface_data})
    for d in joined_data:
        config_file_data['SITENAME'] = d['site_name']
        siteName['siteName'] = d['site_name']
        config_file_data['network'] = ipaddress.IPv4Network(d['destination'] + '/' + d['mask'])
        config_file_data['tunnel_ip'] = d['tunnel_ip']
        config_file_data['tunnel_peer_ip'] = d['tunnel_peer_ip']
    
    configFile = configRequest(**config_file_data)
    
    response = render(request, 'index.html', {'routes': joined_data, 'interfaces': intefaces, 'file_response': configFile, 'siteName': siteName})

    return response
    
    # print(config_file_data)    