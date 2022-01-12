"""
Support certificate management functionality
"""
import logging
from json.decoder import JSONDecodeError
from os import getenv
import urllib.parse
import requests

def delete_cert(common_name):
    "Delete the certificate from Venafi"

    # env vars passed in
    venafi_domain = getenv("VENAFI_DNS_DOMAIN", "venafi.example.com")
    token = getenv("VENAFI_AUTH_TOKEN", "")

    # use auth header for api login
    headers = {
        "Authorization": "Bearer " + token
    }

    # search for cert in venafi
    url_cn = urllib.parse.quote(common_name)
    cert_info_req = requests.get(
        f"https://{venafi_domain}/vedsdk/certificates?cn={url_cn}",
        headers=headers,
        verify='/etc/ssl/certs/ca-certificates.crt'
    )
    status = cert_info_req.status_code

    # error processing below
    if status != 200:
        logging.error(
            "Error getting certificate info for '%s' from Venafi, got status code %s",
            common_name, status)
        return False

    try:
        cert_info = cert_info_req.json()
    except JSONDecodeError:
        logging.error(
            "Could not decode json for '%s', full output: %s",
            common_name, cert_info_req.text)
        return False

    if len(cert_info.get('Certificates', {})) < 1:
        logging.error(
            "Could not find certificate '%s' in Venafi",
            common_name)
        return False

    # get Guid from cert for use in delete api call
    guid = urllib.parse.quote(cert_info['Certificates'][0].get('Guid', '').strip('{}'))

    # call delete api call
    delete_req = requests.delete(
        f"https://{venafi_domain}/vedsdk/certificates/{guid}",
        headers=headers,
        verify='/etc/ssl/certs/ca-certificates.crt'
    )
    status = delete_req.status_code

    if status != 200:
        logging.error(
            "Error getting certificate info for '%s' from Venafi, got status code %s",
            common_name, status)
        return False

    logging.info("Successfully deleted '%s' from Venafi", common_name)
    return True
