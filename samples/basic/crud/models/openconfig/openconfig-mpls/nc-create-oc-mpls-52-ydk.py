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
Create configuration for model openconfig-mpls.

usage: nc-create-oc-mpls-52-ydk.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_mpls \
    as oc_mpls
from ydk.models.openconfig import openconfig_mpls_types as oc_mpls_types
import logging


def config_mpls(mpls):
    """Add config data to mpls object."""
    # auto-bw tunnel
    tunnel = mpls.lsps.constrained_path.Tunnel()
    tunnel.name = "LER1-LER2-t52"
    tunnel.config.name = "LER1-LER2-t52"
    tunnel.config.type = oc_mpls_types.P2PIdentity()
    tunnel.type = oc_mpls_types.P2PIdentity()
    p2p_primary_paths = tunnel.p2p_tunnel_attributes.P2PPrimaryPaths()
    p2p_primary_paths.name = "DYNAMIC"
    p2p_primary_paths.config.name = "DYNAMIC"
    p2p_primary_paths.config.preference = 10
    path_computation_method = oc_mpls.LocallyComputedIdentity()
    p2p_primary_paths.config.path_computation_method = path_computation_method
    tunnel.p2p_tunnel_attributes.p2p_primary_paths.append(p2p_primary_paths)
    tunnel.p2p_tunnel_attributes.config.destination = "172.16.255.2"
    # auto-bandwidth configuration
    tunnel.bandwidth.auto_bandwidth.config.enabled = True
    tunnel.bandwidth.auto_bandwidth.config.min_bw = 10000
    tunnel.bandwidth.auto_bandwidth.config.max_bw = 500000
    tunnel.bandwidth.auto_bandwidth.overflow.config.overflow_threshold = 15
    tunnel.bandwidth.auto_bandwidth.overflow.config.trigger_event_count = 3
    tunnel.bandwidth.auto_bandwidth.underflow.config.underflow_threshold = 15
    tunnel.bandwidth.auto_bandwidth.underflow.config.trigger_event_count = 3

    mpls.lsps.constrained_path.tunnel.append(tunnel)


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

    mpls = oc_mpls.Mpls()  # create object
    config_mpls(mpls)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, mpls)

    exit()
# End of script
