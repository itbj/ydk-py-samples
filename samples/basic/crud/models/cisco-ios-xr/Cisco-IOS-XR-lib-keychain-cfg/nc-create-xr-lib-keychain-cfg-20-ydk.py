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
Create configuration for model Cisco-IOS-XR-lib-keychain-cfg.

usage: nc-create-xr-lib-keychain-cfg-20-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_lib_keychain_cfg \
    as xr_lib_keychain_cfg
import logging


def config_keychains(keychains):
    """Add config data to keychains object."""
    keychain = keychains.Keychain()
    keychain.chain_name = "CHAIN1"
    key = keychain.macsec_keychain.macsec_keys.MacsecKey()
    key.key_id = "10"
    key.macsec_key_string = key.MacsecKeyString()
    key.macsec_key_string.string = "101E584B5643475D5B547B79777C6663754356445055030F0F03055C504C430F0F"
    key.macsec_key_string.cryptographic_algorithm = xr_lib_keychain_cfg.MacsecCryptoAlg.aes_128_cmac
    key.macsec_key_string.encryption_type = xr_lib_keychain_cfg.MacsecEncryption.type7
    key.macsec_lifetime = key.MacsecLifetime()
    key.macsec_lifetime.start_hour = 0
    key.macsec_lifetime.start_minutes = 0
    key.macsec_lifetime.start_seconds = 0
    key.macsec_lifetime.start_date = 1
    key.macsec_lifetime.start_month = xr_lib_keychain_cfg.KeyChainMonth.jan
    key.macsec_lifetime.start_year = 2017
    key.macsec_lifetime.infinite_flag = True
    keychain.macsec_keychain.macsec_keys.macsec_key.append(key)
    keychains.keychain.append(keychain)


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

    keychains = xr_lib_keychain_cfg.Keychains()  # create object
    config_keychains(keychains)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, keychains)

    exit()
# End of script
