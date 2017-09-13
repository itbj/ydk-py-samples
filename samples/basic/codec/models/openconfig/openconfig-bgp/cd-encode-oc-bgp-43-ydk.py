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
Encode configuration for model openconfig-bgp.

usage: cd-encode-oc-bgp-43-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.openconfig import openconfig_bgp \
    as oc_bgp
from ydk.models.openconfig import openconfig_bgp_types as oc_bgp_types
import logging


def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    bgp.global_.config.as_ = 65001
    afi_safi = bgp.global_.afi_safis.AfiSafi()
    afi_safi.afi_safi_name = oc_bgp_types.Ipv6Unicast()
    afi_safi.config.afi_safi_name = oc_bgp_types.Ipv6Unicast()
    afi_safi.config.enabled = True
    bgp.global_.afi_safis.afi_safi.append(afi_safi)

    # configure IBGP peer group
    peer_group = bgp.peer_groups.PeerGroup()
    peer_group.peer_group_name = "IBGP"
    peer_group.config.peer_group_name = "IBGP"
    peer_group.config.peer_as = 65001
    peer_group.transport.config.local_address = "Loopback0"
    afi_safi = peer_group.afi_safis.AfiSafi()
    afi_safi.afi_safi_name = oc_bgp_types.Ipv6Unicast()
    afi_safi.config.afi_safi_name = oc_bgp_types.Ipv6Unicast()
    afi_safi.config.enabled = True
    afi_safi.apply_policy.config.export_policy.append("POLICY2")
    peer_group.afi_safis.afi_safi.append(afi_safi)
    bgp.peer_groups.peer_group.append(peer_group)

    # configure IBGP neighbor
    neighbor = bgp.neighbors.Neighbor()
    neighbor.neighbor_address = "2001:db8::ff:2"
    neighbor.config.neighbor_address = "2001:db8::ff:2"
    neighbor.config.peer_group = "IBGP"
    bgp.neighbors.neighbor.append(neighbor)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    bgp = oc_bgp.Bgp()  # create object
    config_bgp(bgp)  # add object configuration

    # encode and print object
    print(codec.encode(provider, bgp))

    exit()
# End of script
