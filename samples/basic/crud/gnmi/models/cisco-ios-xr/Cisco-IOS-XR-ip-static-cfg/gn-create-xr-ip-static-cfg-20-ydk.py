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
Create configuration for model Cisco-IOS-XR-ip-static-cfg.

usage: gn-create-xr-ip-static-cfg-20-ydk.py [-h] [-v] device

positional arguments:
  device         gNMI device (http://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.path import Repository
from ydk.services import CRUDService
from ydk.gnmi.providers import gNMIServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_static_cfg \
    as xr_ip_static_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_router_static(router_static):
    """Add config data to router_static object."""
    vrf_unicast = router_static.default_vrf.address_family.vrfipv4.vrf_unicast
    vrf_prefix = vrf_unicast.vrf_prefixes.VrfPrefix()
    vrf_prefix.prefix = "0.0.0.0"
    vrf_prefix.prefix_length = 0
    vrf_next_hop_next_hop_address = vrf_prefix.vrf_route.vrf_next_hop_table. \
        VrfNextHopNextHopAddress()
    vrf_next_hop_next_hop_address.next_hop_address = "172.16.1.3"
    vrf_prefix.vrf_route.vrf_next_hop_table.vrf_next_hop_next_hop_address. \
        append(vrf_next_hop_next_hop_address)
    vrf_unicast.vrf_prefixes.vrf_prefix.append(vrf_prefix)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="gNMI device (http://user:password@host:port)")
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

    # create gNMI provider
    repository = Repository(YDK_REPO_DIR+device.hostname)
    provider = gNMIServiceProvider(repo=repository,
                                   address=device.hostname,
                                   port=device.port,
                                   username=device.username,
                                   password=device.password)
    # create CRUD service
    crud = CRUDService()

    router_static = xr_ip_static_cfg.RouterStatic()  # create object
    config_router_static(router_static)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, router_static)

    exit()
# End of script
