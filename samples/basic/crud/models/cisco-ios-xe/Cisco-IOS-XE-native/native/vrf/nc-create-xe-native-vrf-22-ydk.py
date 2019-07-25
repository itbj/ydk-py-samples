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
Create configuration for model Cisco-IOS-XE-native.
usage: nc-create-xe-native-20-ydk.py [-h] [-v] device
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
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native \
    as xe_native
import logging


def config_native(native):
    """Add config data to native object."""
    definition = native.vrf.Definition()
    definition.name = "VRF2"
    definition.rd = "65000:2"
    definition.description = "IPv6 VRF with Route Target"

    # Address-Family Creation
    ipv6 = definition.address_family.Ipv6()
    ipv6.parent = definition.address_family

    # Route Target Creation
    export = ipv6.route_target.Export()
    export.asn_ip = "65000:2"
    import_ = ipv6.route_target.Import()
    import_.asn_ip = "65000:2"

    ipv6.route_target.export.append(export)
    ipv6.route_target.import_.append(import_)

    definition.address_family.ipv6 = ipv6

    native.vrf.definition.append(definition)


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

    native = xe_native.Native()  # create object
    config_native(native)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, native)

    #provider.close()
    exit()
# End of script
