import json
import sys
from typing import TextIO

from src.clients.device_test_client import DeviceTestClient
from src.clients.hardware_manager_client import HardwareManagerClient

indent = 4

def run_eyepatch_calibration_impl(esn: str, audio_source: str, eyepatch_serial: str, out_file: TextIO, net_key: str, use_netflix_access: bool):
    device_test_client = DeviceTestClient(net_key, use_netflix_access)
    hardware_manager_client = HardwareManagerClient(net_key, use_netflix_access)

    # Get device details to retrieve host hardware serial
    device_details = device_test_client.get_registry_device_details(esn)
    host = device_details.get("hardware_serial")
    # Get peripherals connected to the host
    peripherals = hardware_manager_client.get_host_peripherals(host)

    # Check if any peripheral is an old Eyepatch
    has_old_eyepatch = any(
        peripheral.get("hw_config", {}).get("type", "").lower() == "eyepatch"
        for peripheral in peripherals
    )

    if has_old_eyepatch:
        print(
            "\nWarning: the EyePatch sensor being used currently is marked for deprecation on Jan 31, 2026.\n\n"
            "Calibration will be able to complete for these legacy hexagonal sensors until this time.\n\n"
            "To procure a new sensor (EyePatch Ultra) please navigate to the following ordering site:\n"
            "https://docs.netflixpartners.com/docs/nrdp/cert/setting-up-nts/eyepatch-ultra/order-form/\n\n"
            "If there are questions or concerns, please reach out to your Netflix Partner Engineering contact for more information.\n",
            file=sys.stderr
        )

    plan = device_test_client.get_eyepatch_calibration_plan(esn, audio_source, eyepatch_serial)
    run_summary = device_test_client.run_test_plan(plan, True)

    json.dump(run_summary, out_file, indent=indent)
