#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Create configuration for model openconfig-telemetry.

usage: config_telemetry.py [-h] [-v] destination device

positional arguments:
  destination    destination for telemetry data stream
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.openconfig import openconfig_telemetry as oc_telemetry
import logging


def config_telemetry_system(telemetry_system, destination_address):
    """Add config data to telemetry_system object."""
    # configure sensor group
    sensor_group = telemetry_system.sensor_groups.SensorGroup()
    sensor_group.sensor_group_id = "PEERING-SENSORS"
    sensor_group.config.sensor_group_id = "PEERING-SENSORS"
    # configure  interface sensor path
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "openconfig-interfaces:interfaces/interface"
    sensor_path.config.path = "openconfig-interfaces:interfaces/interface"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    # configure bgp-neighbor sensor path
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "openconfig-bgp:bgp/neighbors"
    sensor_path.config.path = "openconfig-bgp:bgp/neighbors"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_system.sensor_groups.sensor_group.append(sensor_group)

    # configure destination group
    destination_group = telemetry_system.destination_groups.DestinationGroup()
    destination_group.group_id = "PIPELINE"
    destination_group.config.group_id = "PIPELINE"
    # configure destination
    destination = destination_group.destinations.Destination()
    destination.destination_address = destination_address
    destination.destination_port = 5432
    destination.config.destination_address = destination_address
    destination.config.destination_port = 5432
    destination.config.destination_protocol = oc_telemetry.TelemetryStreamProtocolEnum.TCP
    destination_group.destinations.destination.append(destination)
    telemetry_system.destination_groups.destination_group.append(destination_group)

    # configure subscription
    subscription = telemetry_system.subscriptions.persistent.Subscription()
    subscription.subscription_id = 10
    subscription.config.subscription_id = 10
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensor_group = "PEERING-SENSORS"
    sensor_profile.config.sensor_group = "PEERING-SENSORS"
    sensor_profile.config.sample_interval = 10000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    destination_group = subscription.destination_groups.DestinationGroup()
    destination_group.group_id = "PIPELINE"
    destination_group.config.group_id = "PIPELINE"
    subscription.destination_groups.destination_group.append(destination_group)
    telemetry_system.subscriptions.persistent.subscription.append(subscription)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("destination",
                        help="destination for telemetry data stream")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    telemetry_system = oc_telemetry.TelemetrySystem()  # create object
    config_telemetry_system(telemetry_system,
                            destination_address=args.destination)

    # create configuration on NETCONF device
    crud.create(provider, telemetry_system)

    provider.close()
    exit()
# End of script
