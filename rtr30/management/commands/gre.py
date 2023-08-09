import paramiko,re

def find_tun_interfaces(rtr):
    stdin, stdout, stderr = rtr.exec_command('show ip int brief | i Tunnel')
    config = stdout.read().decode('utf-8')

    tunnel_interfaces = re.findall(r'Tunnel\d+', config)

    return tunnel_interfaces

def get_tun_interface(rtr,interface=None):
    import ipaddress

    stdin, stdout, stderr = rtr.exec_command(f'show run interface {interface}')
    config = stdout.read().decode('utf-8')

    # Define the regular expression patterns
    description_pattern = r'description (.+)'
    ip_address_pattern = r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)'
    tunnel_destination_pattern = r'tunnel destination (\S+)'
    tunnel_vrf_pattern = r'tunnel vrf (\S+)'

    # Search for the interface information
    description_match = re.search(description_pattern, config)
    ip_address_match = re.search(ip_address_pattern, config)
    tunnel_destination_match = re.search(tunnel_destination_pattern, config)
    tunnel_vrf_match = re.search(tunnel_vrf_pattern, config)

    # Extract the interface details
    description = description_match.group(1) if description_match else None
    tunnel_ip = ip_address_match.group(1) if ip_address_match else None
    subnet_mask = ip_address_match.group(2) if ip_address_match else None
    tunnel_destination = tunnel_destination_match.group(1) if tunnel_destination_match else None
    tunnel_vrf = tunnel_vrf_match.group(1) if tunnel_vrf_match else None

    network = ipaddress.IPv4Address(tunnel_ip)
    next_ip = network + 1

    # Print the extracted details
    info_dict = {
        "Description": description.replace('\r', ''),
        "Peer IP": str(next_ip),
        "Tunnel IP": tunnel_ip,
        "Subnet Mask": subnet_mask,
        "LTE IP": tunnel_destination,
        "VRF": tunnel_vrf
    }
    return info_dict



def get_tun_routes(rtr,interface=None):
    import ipaddress
    stdin, stdout, stderr = rtr.exec_command(f'sh run | i ^ip route .* {interface}$')
    # stdin, stdout, stderr = rtr.exec_command(f'show run | i {interface}')
    config = stdout.read().decode('utf-8')
    route_pattern = r'ip route vrf (\S+) (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+) (Tunnel\d+)'

    # Search for the interface and route information
    route_matches = re.findall(route_pattern, config)

    # Extract the route details
    if len(route_matches) > 0:
        routes = []
        for match in route_matches:
            vrf = match[0]
            destination = match[1]
            mask = match[2]
            tunnel_interface = match[3]
            network = ipaddress.IPv4Address(destination)
            gateway_ip = network + 1
            first_ip = gateway_ip + 1
            routes.append((vrf, str(gateway_ip), str(first_ip), destination, mask, tunnel_interface))

        return routes
    else:
        print('No routes found!')


def login(data=False):
    from secretkeys import rtr30_pass
    host = '10.1.110.123'
    port = 22
    username = 'nmohan'
    password = rtr30_pass
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password, allow_agent=False, look_for_keys=False)
    return ssh