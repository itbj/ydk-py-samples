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

usage: gn-create-xr-lib-keychain-cfg-24-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_lib_keychain_cfg \
    as xr_lib_keychain_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_keychains(keychains):
    """Add config data to keychains object."""
    keychain = keychains.Keychain()
    keychain.chain_name = "CHAIN3"
    key = keychain.macsec_keychain.macsec_keys.MacsecKey()
    key.key_id = "10"
    key.macsec_key_string = key.MacsecKeyString()
    key.macsec_key_string.string = "01435756085F5359761C1F5B4A5142445C5C557878707D6562724255455754000E0802065D574D400E0806010101015D0C56560A04504650530B5A545C7519185E"
    key.macsec_key_string.cryptographic_algorithm = xr_lib_keychain_cfg.MacsecCryptoAlg.aes_256_cmac
    key.macsec_key_string.encryption_type = xr_lib_keychain_cfg.MacsecEncryption.type7
    key.macsec_lifetime = key.MacsecLifetime()
    key.macsec_lifetime.start_hour = 0
    key.macsec_lifetime.start_minutes = 0
    key.macsec_lifetime.start_seconds = 0
    key.macsec_lifetime.start_date = 1
    key.macsec_lifetime.start_month = xr_lib_keychain_cfg.KeyChainMonth.jan
    key.macsec_lifetime.start_year = 2017
    key.macsec_lifetime.end_hour = 23
    key.macsec_lifetime.end_minutes = 59
    key.macsec_lifetime.end_seconds = 59
    key.macsec_lifetime.end_date = 7
    key.macsec_lifetime.end_month = xr_lib_keychain_cfg.KeyChainMonth.jan
    key.macsec_lifetime.end_year = 2017
    keychain.macsec_keychain.macsec_keys.macsec_key.append(key)

    # Second key
    key = keychain.macsec_keychain.macsec_keys.MacsecKey()
    key.key_id = "20"
    key.macsec_key_string = key.MacsecKeyString()
    key.macsec_key_string.string = "04035C505A751F1C58415241475F5F567B73737E66617141564E5457030D0B010556544E430D0B05020A02025E0F5555090F5345535008595757761A1B5D4A5746"
    key.macsec_key_string.cryptographic_algorithm = xr_lib_keychain_cfg.MacsecCryptoAlg.aes_256_cmac
    key.macsec_key_string.encryption_type = xr_lib_keychain_cfg.MacsecEncryption.type7
    key.macsec_lifetime = key.MacsecLifetime()
    key.macsec_lifetime.start_hour = 23
    key.macsec_lifetime.start_minutes = 0
    key.macsec_lifetime.start_seconds = 0
    key.macsec_lifetime.start_date = 7
    key.macsec_lifetime.start_month = xr_lib_keychain_cfg.KeyChainMonth.jan
    key.macsec_lifetime.start_year = 2017
    key.macsec_lifetime.end_hour = 23
    key.macsec_lifetime.end_minutes = 59
    key.macsec_lifetime.end_seconds = 59
    key.macsec_lifetime.end_date = 13
    key.macsec_lifetime.end_month = xr_lib_keychain_cfg.KeyChainMonth.jan
    key.macsec_lifetime.end_year = 2017
    keychain.macsec_keychain.macsec_keys.macsec_key.append(key)
    keychains.keychain.append(keychain)


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

    keychains = xr_lib_keychain_cfg.Keychains()  # create object
    config_keychains(keychains)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, keychains)

    exit()
# End of script
