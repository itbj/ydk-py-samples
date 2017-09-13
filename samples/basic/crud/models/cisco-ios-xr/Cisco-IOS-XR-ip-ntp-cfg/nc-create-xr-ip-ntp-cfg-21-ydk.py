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
Create configuration for model Cisco-IOS-XR-ip-ntp-cfg.

usage: nc-create-xr-ip-ntp-cfg-21-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_ntp_cfg \
    as xr_ip_ntp_cfg
import logging


def config_ntp(ntp):
    """Add config data to ntp object."""
    peer_vrf = ntp.peer_vrfs.PeerVrf()
    peer_vrf.vrf_name = "default"
    peer_ipv6 = peer_vrf.peer_ipv6s.PeerIpv6()
    peer_ipv6.address_ipv6 = "2001:db8::a:1"
    peer_type_ipv6 = peer_ipv6.PeerTypeIpv6()
    peer_type_ipv6.peer_type = xr_ip_ntp_cfg.NtpPeer.server
    peer_ipv6.peer_type_ipv6.append(peer_type_ipv6)
    peer_vrf.peer_ipv6s.peer_ipv6.append(peer_ipv6)
    ntp.peer_vrfs.peer_vrf.append(peer_vrf)


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

    ntp = xr_ip_ntp_cfg.Ntp()  # create object
    config_ntp(ntp)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, ntp)

    exit()
# End of script
