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
Create configuration for model openconfig-interfaces.

usage: config_interfaces.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_interfaces as oc_interfaces
import logging


def config_interfaces(interfaces, name, description, address_ip, prefix_length):
    """Add config data to interfaces object."""
    # configure interface
    interface = interfaces.Interface()
    interface.name = name
    interface.config.name = name
    interface.config.description = description
    interface.config.enabled = True

    # configure ip subinterface
    subinterface = interface.subinterfaces.Subinterface()
    subinterface.index = 0
    subinterface.config.index = 0
    subinterface.ipv4 = subinterface.Ipv4()
    address = subinterface.ipv4.Address()
    address.ip = address_ip
    address.config.ip = address_ip
    address.config.prefix_length = prefix_length
    subinterface.ipv4.address.append(address)
    interface.subinterfaces.subinterface.append(subinterface)
    interfaces.interface.append(interface)


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

    interfaces = oc_interfaces.Interfaces()  # create object
    config_interfaces(interfaces,
                      name="GigabitEthernet0/0/0/0",
                      description="Peering with AS65002",
                      address_ip="192.168.0.1",
                      prefix_length=24)

    # create configuration on NETCONF device
    crud.create(provider, interfaces)

    provider.close()
    exit()
# End of script
