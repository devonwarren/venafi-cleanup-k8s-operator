"""
Main Kopf Runtime source code
"""

import logging
import kopf
from certificates import delete_cert

@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    "Configure Kopf"
    settings.persistence.finalizer = 'venafi-cleanup-operator'

@kopf.on.delete('certificates')
def venafi_cert_clean(body, **_):
    "Remove k8s deleted certificates in venafi"

    common_name = body.get("spec", {}).get("commonName", "")

    if common_name == "":
        logging.error("Could not get commonName for cert: %s", body)
        return False

    # delete the certificate from venafi
    delete_status = delete_cert(common_name)

    if not delete_status:
        fail_msg = f"Failed to removed '{common_name}' certificate from Venafi"
        kopf.warn(body, reason="VenafiCleanUp", message=fail_msg)
        return False

    success_msg = f"Successfully removed '{common_name}' certificate from Venafi"
    kopf.info(body, reason="VenafiCleanUp", message=success_msg)
    return True
