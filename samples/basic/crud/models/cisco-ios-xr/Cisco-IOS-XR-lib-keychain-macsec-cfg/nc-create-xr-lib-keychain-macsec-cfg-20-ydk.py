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
Create configuration for model Cisco-IOS-XR-lib-keychain-macsec-cfg.

usage: nc-create-xr-lib-keychain-macsec-cfg-20-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_lib_keychain_macsec_cfg \
    as xr_lib_keychain_macsec_cfg
import logging


def config_mac_sec_keychains(mac_sec_keychains):
    """Add config data to mac_sec_keychains object."""
    mac_sec_keychain = mac_sec_keychains.MacSecKeychain()
    mac_sec_keychain.chain_name = "CHAIN1"
    key = mac_sec_keychain.keies.Key()
    key.key_id = "10"
    key.key_string = key.KeyString()
    key.key_string.string = "101E584B5643475D5B547B79777C6663754356445055030F0F03055C504C430F0F"
    key.key_string.cryptographic_algorithm = xr_lib_keychain_macsec_cfg.MacSecCryptoAlgEnum.aes_128_cmac
    key.lifetime.start_hour = 0
    key.lifetime.start_minutes = 0
    key.lifetime.start_seconds = 0
    key.lifetime.start_date = 1
    key.lifetime.start_month = xr_lib_keychain_macsec_cfg.MacSecKeyChainMonthEnum.jan
    key.lifetime.start_year = 2017
    key.lifetime.infinite_flag = True
    mac_sec_keychain.keies.key.append(key)
    mac_sec_keychains.mac_sec_keychain.append(mac_sec_keychain)


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

    mac_sec_keychains = xr_lib_keychain_macsec_cfg.MacSecKeychains()  # create object
    config_mac_sec_keychains(mac_sec_keychains)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, mac_sec_keychains)

    exit()
# End of script
