#!/usr/bin/env python3
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
Remove configuration for BGP peer.

usage: remove_bgp_peer.py [-h] [-v] local_as peer_address device

positional arguments:
  local_as       local autonomous system
  peer_address   peer address
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

import argparse
import urllib.parse
import sys
import logging
import os

from ydk.models.openconfig import openconfig_network_instance as oc_network_instance
from ydk.models.openconfig import openconfig_bgp as oc_bgp
from ydk.models.openconfig import openconfig_policy_types as oc_policy_types
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.filters import YFilter


def bgp_peer_remove_filter(network_instances, local_as, peer_address):
    "Define filter to remove BGP peer"
    # configure default network instance
    network_instance = network_instances.NetworkInstance()
    network_instance.name = "default"
   
    # configure BGP
    protocol = network_instance.protocols.Protocol()
    protocol.identifier = oc_policy_types.BGP()
    protocol.name = "default"

    protocol.bgp.global_.config.as_ = local_as
    neighbor = protocol.bgp.neighbors.Neighbor()
    neighbor.neighbor_address = peer_address
    neighbor.yfilter = YFilter.remove

    protocol.bgp.neighbors.neighbor.append(neighbor)
    network_instance.protocols.protocol.append(protocol)
    network_instances.network_instance.append(network_instance)


if __name__ == "__main__":
    """Execute main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", 
                        help="print debugging messages",
                        action="store_true")
    parser.add_argument("local_as",
                        help="local autonomous system")
    parser.add_argument("peer_address",
                        help="peer address")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urllib.parse.urlparse(args.device)

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

    # BGP configuration filter
    network_instances = oc_network_instance.NetworkInstances()
    bgp_peer_remove_filter(network_instances, int(args.local_as), args.peer_address)

    # update configuration on NETCONF device
    crud.update(provider, network_instances)

    exit()
# End of script
