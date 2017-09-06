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
Execute RPC for model Cisco-IOS-XR-snmp-test-trap-act.

usage: nc-execute-xr-snmp-test-trap-act-426-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import ExecutorService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_snmp_test_trap_act \
    as xr_snmp_test_trap_act
import logging


def prepare_entity_fru_fan_tray_removed_rpc(entity_fru_fan_tray_removed_rpc):
    """Add RPC input data to entity_fru_fan_tray_removed_rpc object."""
    entity_fru_fan_tray_removed_rpc.input.entindex = 5


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
    # create executor service
    executor = ExecutorService()

    entity_fru_fan_tray_removed_rpc = xr_snmp_test_trap_act.EntityFruFanTrayRemovedRpc()  # create object
    prepare_entity_fru_fan_tray_removed_rpc(entity_fru_fan_tray_removed_rpc)  # add RPC input

    # execute RPC on NETCONF device
    executor.execute_rpc(provider, entity_fru_fan_tray_removed_rpc)

    exit()
# End of script
