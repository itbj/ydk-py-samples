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
Create configuration for model Cisco-IOS-XR-ip-rsvp-cfg.

usage: nc-create-xr-ip-rsvp-cfg-24-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_rsvp_cfg \
    as xr_ip_rsvp_cfg
from ydk.types import Empty
import logging


def config_rsvp(rsvp):
    """Add config data to rsvp object."""
    # RSVP interface gig0/0/0/0
    interface = rsvp.interfaces.Interface()
    interface.name = "GigabitEthernet0/0/0/0"
    interface.bandwidth.rdm.bc0_bandwidth = 100
    interface.bandwidth.rdm.bc1_bandwidth = 25
    interface.bandwidth.rdm.rdm_keyword = xr_ip_rsvp_cfg.RsvpRdm.rdm
    interface.bandwidth.rdm.bc0_keyword = xr_ip_rsvp_cfg.RsvpBc0.not_specified
    interface.bandwidth.rdm.bc1_keyword = xr_ip_rsvp_cfg.RsvpBc1.sub_pool
    interface.bandwidth.rdm.bandwidth_mode = xr_ip_rsvp_cfg.RsvpBwCfg.percentage
    rsvp.interfaces.interface.append(interface)

    # RSVP interface gig0/0/0/1
    interface = rsvp.interfaces.Interface()
    interface.name = "GigabitEthernet0/0/0/1"
    interface.bandwidth.rdm.bc0_bandwidth = 100
    interface.bandwidth.rdm.bc1_bandwidth = 25
    interface.bandwidth.rdm.rdm_keyword = xr_ip_rsvp_cfg.RsvpRdm.rdm
    interface.bandwidth.rdm.bc0_keyword = xr_ip_rsvp_cfg.RsvpBc0.not_specified
    interface.bandwidth.rdm.bc1_keyword = xr_ip_rsvp_cfg.RsvpBc1.sub_pool
    interface.bandwidth.rdm.bandwidth_mode = xr_ip_rsvp_cfg.RsvpBwCfg.percentage
    rsvp.interfaces.interface.append(interface)


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

    rsvp = xr_ip_rsvp_cfg.Rsvp()  # create object
    config_rsvp(rsvp)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, rsvp)

    exit()
# End of script
