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
Create configuration for model Cisco-IOS-XR-ipv4-arp-cfg.

usage: nc-create-xr-ipv4-arp-cfg-32-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_arp_cfg \
    as xr_ipv4_arp_cfg
import logging


def config_arpgmp(arpgmp):
    """Add config data to arpgmp object."""
    vrf = arpgmp.Vrf()
    vrf.vrf_name = "default"

    # arp entry for 172.16.0.1
    entry = vrf.entries.Entry()
    entry.address = "172.16.0.1"
    entry.mac_address = "52:54:00:28:89:88"
    entry.encapsulation = xr_ipv4_arp_cfg.ArpEncapEnum.arpa
    entry.entry_type = xr_ipv4_arp_cfg.ArpEntryEnum.static
    vrf.entries.entry.append(entry)

    # arp entry for 172.16.0.4
    entry = vrf.entries.Entry()
    entry.address = "172.16.0.4"
    entry.mac_address = "52:54:00:7d:8f:8f"
    entry.encapsulation = xr_ipv4_arp_cfg.ArpEncapEnum.arpa
    entry.entry_type = xr_ipv4_arp_cfg.ArpEntryEnum.static
    vrf.entries.entry.append(entry)
    arpgmp.vrf.append(vrf)


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

    arpgmp = xr_ipv4_arp_cfg.Arpgmp()  # create object
    config_arpgmp(arpgmp)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, arpgmp)

    exit()
# End of script
