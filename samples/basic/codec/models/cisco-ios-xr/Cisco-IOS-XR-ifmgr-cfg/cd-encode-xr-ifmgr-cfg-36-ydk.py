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
Encode configuration for model Cisco-IOS-XR-ifmgr-cfg.

usage: cd-encode-xr-ifmgr-cfg-36-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg \
    as xr_ifmgr_cfg
import logging


def config_interface_configurations(interface_configurations):
    """Add config data to interface_configurations object."""
    # configure IPv6 loopback
    interface_configuration = interface_configurations.InterfaceConfiguration()
    interface_configuration.active = "act"
    interface_configuration.interface_name = "GigabitEthernet0/0/0/0"
    interface_configuration.description = "CONNECTS TO LSR1 (g0/0/0/1)"
    mtu = interface_configuration.mtus.Mtu()
    mtu.owner = "GigabitEthernet"
    mtu.mtu = 9192
    interface_configuration.mtus.mtu.append(mtu)
    addresses = interface_configuration.ipv6_network.addresses
    regular_address = addresses.regular_addresses.RegularAddress()
    regular_address.address = "2001:db8::1:0"
    regular_address.prefix_length = 127
    addresses.regular_addresses.regular_address.append(regular_address)
    interface_configuration.statistics.load_interval = 30
    interface_configurations.interface_configuration.append(interface_configuration)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()  # create object
    config_interface_configurations(interface_configurations)  # add object configuration

    # encode and print object
    print(codec.encode(provider, interface_configurations))

    exit()
# End of script
