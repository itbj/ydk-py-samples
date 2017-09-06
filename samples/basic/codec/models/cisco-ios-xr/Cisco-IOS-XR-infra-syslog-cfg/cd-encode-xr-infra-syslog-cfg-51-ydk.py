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
Encode configuration for model Cisco-IOS-XR-infra-syslog-cfg.

usage: cd-encode-xr-infra-syslog-cfg-51-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_syslog_cfg \
    as xr_infra_syslog_cfg
import logging


def config_syslog(syslog):
    """Add config data to syslog_service object."""
    #Facility
    syslog.logging_facilities.facility_level = xr_infra_syslog_cfg.FacilityEnum.local0

    #Hostserver
    vrf = syslog.host_server.vrfs.Vrf()
    vrf.vrf_name = "default"
    ipv6 = vrf.ipv6s.Ipv6()
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

    syslog = xr_infra_syslog_cfg.Syslog()  # create object
    config_syslog(syslog)  # add object configuration

    # encode and print object
    print(codec.encode(provider, syslog))

    exit()
# End of script
