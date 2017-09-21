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
#

"""
Create configuration for model Cisco-IOS-XR-ipv6-ospfv3-cfg.

usage: nc-create-xr-ipv6-ospfv3-cfg-30-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv6_ospfv3_cfg \
    as xr_ipv6_ospfv3_cfg
from ydk.types import Empty
import logging


def config_ospfv3(ospfv3):
    """Add config data to ospfv3 object."""
    # OSPFv3 process
    process = ospfv3.processes.Process()
    process.process_name = "DEFAULT"
    process.default_vrf.router_id = "172.16.255.101"
    process.enable = Empty()

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0
    area_area_id.enable = Empty()

    # loopback interface passive
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "Loopback0"
    interface.enable = Empty()
    interface.passive = True
    area_area_id.interfaces.interface.append(interface)

    # gi0/0/0/0 interface
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "GigabitEthernet0/0/0/0"
    interface.enable = Empty()
    interface.network = xr_ipv6_ospfv3_cfg.Ospfv3Network.point_to_point
    area_area_id.interfaces.interface.append(interface)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # Area 1
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 1
    area_area_id.enable = Empty()

    # gi0/0/0/0 interface
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "GigabitEthernet0/0/0/1"
    interface.enable = Empty()
    interface.network = xr_ipv6_ospfv3_cfg.Ospfv3Network.point_to_point
    area_area_id.interfaces.interface.append(interface)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # append process config
    ospfv3.processes.process.append(process)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
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

    ospfv3 = xr_ipv6_ospfv3_cfg.Ospfv3()  # create object
    config_ospfv3(ospfv3)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, ospfv3)

    exit()
# End of script
