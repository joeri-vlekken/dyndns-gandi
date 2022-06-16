import ipaddress
import requests


# Validation of IP addresses
def validate_ip(version: int, address: str):
    try:
        ip_address = ipaddress.ip_address(address)
        if isinstance(ip_address, ipaddress.IPv4Address) and version == 4:
            return ip_address
        elif isinstance(ip_address, ipaddress.IPv6Address) and version == 6:
            return ip_address
    except ValueError:
        return False


# Update the record at Linode DNS Manager
def update_record(
        ipv4: ipaddress.IPv4Address,
        ipv6: ipaddress.IPv6Address,
        token: str,
        domain: str,
        record: str,
        ttl: int
):
    api_url = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{record}"
    headers = {
        'Authorization': 'Apikey ' + token,
        'Content-Type': 'application/json'
    }

    # Update the record
    print(f'update record: {address}')
    data = {
        "items": []
    }
    if ipv4:
        data['items'].append(
            {
                "rrset_name": record,
                "rrset_type": "A",
                "rrset_ttl": 300,
                "rrset_values": [
                    str(ipv4)
                ]
            }
        )
    if ipv6:
        data['items'].append(
            {
                "rrset_name": record,
                "rrset_type": "AAAA",
                "rrset_ttl": 300,
                "rrset_values": [
                    str(ipv6)
                ]
            }
        )
    try:
        updated_record = requests.put(api_url, headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        return {'success': False, 'msg': f'Gandi API error: {str(e)}'}

    return {'success': True, 'msg': updated_record.json()}
