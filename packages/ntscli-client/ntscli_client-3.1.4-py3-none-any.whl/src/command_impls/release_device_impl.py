import json
from typing import TextIO

from src.clients.device_test_client import DeviceTestClient

indent = 4

def release_device_impl(esn: str, out_file: TextIO, net_key: str, use_netflix_access: bool):
    device_test_client = DeviceTestClient(net_key, use_netflix_access)
    registry_device_details = device_test_client.get_registry_device_details(esn)

    user = registry_device_details["user"]
    message = "device is not reserved"

    if user is not None:
        device_test_client.release_device_reservation(esn, user)
        message = "manually released device reservation"

    result = {
        "message": message
    }

    json.dump(result, out_file, indent=indent)
