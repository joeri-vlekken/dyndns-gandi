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
    print(f'update record: {record} at {domain}')
    update_list = []

    if ipv4:
        update_list.append(
            {
                "type": "A",
                "data": {
                    "rrset_values": [
                        str(ipv4)
                    ],
                    "rrset_ttl": ttl
                }
            }
        )
    if ipv6:
        update_list.append(
            {
                "type": "AAAA",
                "data": {
                    "rrset_values": [
                        str(ipv6)
                    ],
                    "rrset_ttl": ttl
                }
            }
        )

    result = []
    print(update_list)
    for update in update_list:
        try:
            updated_record = requests.put(
                f'{api_url}/{update["type"]}', headers=headers, json=update['data'])
        except requests.exceptions.RequestException as e:
            result.append(str(e))
            continue
        result.append(updated_record.json())

    return result
