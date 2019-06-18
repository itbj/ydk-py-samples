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
Encode configuration for model openconfig-mpls.

usage: cd-encode-oc-mpls-58-ydk.py [-h] [-v] device


optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.openconfig import openconfig_network_instance \
    as oc_network_instance
from ydk.models.openconfig import openconfig_mpls_types \
    as oc_mpls_types
import logging


def config_mpls(network_instances):
    """Add config data to mpls object."""
    # configure default network instance
    network_instance = network_instances.NetworkInstance()
    network_instance.name = "default"
    network_instance.config.name = "default"

    # tunnel with explicit and dynamic path options
    tunnel = network_instance.mpls.lsps.constrained_path.tunnels.Tunnel()
    tunnel.name = "LER1-LER2-t58"
    tunnel.config.name = "LER1-LER2-t58"
    tunnel.config.type = oc_mpls_types.P2P()
    #tunnel.type = oc_mpls_types.P2P()
    # explicit path
    p2p_primary_path = tunnel.p2p_tunnel_attributes.p2p_primary_path.P2pPrimaryPath_()
    p2p_primary_path.name = "LER1-LSR1-LER2"
    p2p_primary_path.config.name = "LER1-LSR1-LER2"
    p2p_primary_path.config.preference = 10
    p2p_primary_path.config.explicit_path_name = "LER1-LSR1-LER2"
    path_computation_method = oc_mpls_types.EXPLICITLYDEFINED()
    p2p_primary_path.config.path_computation_method = path_computation_method
    tunnel.p2p_tunnel_attributes.p2p_primary_path.p2p_primary_path.append(p2p_primary_path)
    # dynamic path
    p2p_primary_path = tunnel.p2p_tunnel_attributes.p2p_primary_path.P2pPrimaryPath_()
    p2p_primary_path.name = "DYNAMIC"
    p2p_primary_path.config.name = "DYNAMIC"
    p2p_primary_path.config.preference = 20
    path_computation_method = oc_mpls_types.LOCALLYCOMPUTED()
    p2p_primary_path.config.path_computation_method = path_computation_method
    tunnel.p2p_tunnel_attributes.p2p_primary_path.p2p_primary_path.append(p2p_primary_path)
    tunnel.p2p_tunnel_attributes.config.destination = "172.16.255.2"
    tunnel.bandwidth.config.set_bandwidth = 100000

    network_instance.mpls.lsps.constrained_path.tunnels.tunnel.append(tunnel)
    network_instances.network_instance.append(network_instance)


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

    network_instances = oc_network_instance.NetworkInstances()
    config_mpls(network_instances)  # add object configuration

    # encode and print object
    print(codec.encode(provider, network_instances))

    exit()
# End of script
