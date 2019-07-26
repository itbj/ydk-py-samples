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
Create configuration for model Cisco-IOS-XR-infra-syslog-cfg.

usage: gn-create-xr-infra-syslog-cfg-51-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_syslog_cfg \
    as xr_infra_syslog_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_syslog(syslog):
    """Add config data to syslog object."""
    #Facility
    syslog.logging_facilities.facility_level = xr_infra_syslog_cfg.Facility.local0

    #Hostserver
    vrf = syslog.host_server.vrfs.Vrf()
    vrf.vrf_name = "default"
    ipv6 = vrf.ipv6s.Ipv6()
    ipv6.ipv6_severity_port = ipv6.Ipv6SeverityPort()
    ipv6.address = "2001:db8::a:1"
    vrf.ipv6s.ipv6.append(ipv6)
    syslog.host_server.vrfs.vrf.append(vrf)

    #Source-interface
    source_interface_value = syslog.source_interface_table.source_interface_values.SourceInterfaceValue()
    source_interface_value.src_interface_name_value = "Loopback0"
    source_interface_vrf = source_interface_value.source_interface_vrfs.SourceInterfaceVrf()
    source_interface_vrf.vrf_name = "default"
    source_interface_value.source_interface_vrfs.source_interface_vrf.append(source_interface_vrf)
    syslog.source_interface_table.source_interface_values.source_interface_value.append(source_interface_value)


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

    syslog = xr_infra_syslog_cfg.Syslog()  # create object
    config_syslog(syslog)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, syslog)

    exit()
# End of script
