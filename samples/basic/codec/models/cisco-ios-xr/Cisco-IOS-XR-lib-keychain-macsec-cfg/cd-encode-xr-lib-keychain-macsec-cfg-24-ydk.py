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
Encode configuration for model Cisco-IOS-XR-lib-keychain-macsec-cfg.

usage: cd-encode-xr-lib-keychain-macsec-cfg-24-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_lib_keychain_macsec_cfg \
    as xr_lib_keychain_macsec_cfg
import logging


def config_mac_sec_keychains(mac_sec_keychains):
    """Add config data to mac_sec_keychains object."""
    mac_sec_keychain = mac_sec_keychains.MacSecKeychain()
    mac_sec_keychain.chain_name = "CHAIN3"
    key = mac_sec_keychain.keies.Key()
    key.key_id = "10"
    key.key_string = key.KeyString()
    key.key_string.string = "01435756085F5359761C1F5B4A5142445C5C557878707D6562724255455754000E0802065D574D400E0806010101015D0C56560A04504650530B5A545C7519185E"
    key.key_string.cryptographic_algorithm = xr_lib_keychain_macsec_cfg.MacSecCryptoAlg.aes_256_cmac
    key.lifetime.start_hour = 0
    key.lifetime.start_minutes = 0
    key.lifetime.start_seconds = 0
    key.lifetime.start_date = 1
    key.lifetime.start_month = xr_lib_keychain_macsec_cfg.MacSecKeyChainMonth.jan
    key.lifetime.start_year = 2017
    key.lifetime.end_hour = 23
    key.lifetime.end_minutes = 59
    key.lifetime.end_seconds = 59
    key.lifetime.end_date = 7
    key.lifetime.end_month = xr_lib_keychain_macsec_cfg.MacSecKeyChainMonth.jan
    key.lifetime.end_year = 2017
    key.lifetime.infinite_flag = False
    mac_sec_keychain.keies.key.append(key)

    # Second key
    key = mac_sec_keychain.keies.Key()
    key.key_id = "20"
    key.key_string = key.KeyString()
    key.key_string.string = "04035C505A751F1C58415241475F5F567B73737E66617141564E5457030D0B010556544E430D0B05020A02025E0F5555090F5345535008595757761A1B5D4A5746"
    key.key_string.cryptographic_algorithm = xr_lib_keychain_macsec_cfg.MacSecCryptoAlg.aes_256_cmac
    key.lifetime.start_hour = 23
    key.lifetime.start_minutes = 0
    key.lifetime.start_seconds = 0
    key.lifetime.start_date = 7
    key.lifetime.start_month = xr_lib_keychain_macsec_cfg.MacSecKeyChainMonth.jan
    key.lifetime.start_year = 2017
    key.lifetime.end_hour = 23
    key.lifetime.end_minutes = 59
    key.lifetime.end_seconds = 59
    key.lifetime.end_date = 13
    key.lifetime.end_month = xr_lib_keychain_macsec_cfg.MacSecKeyChainMonth.jan
    key.lifetime.end_year = 2017
    key.lifetime.infinite_flag = False
    mac_sec_keychain.keies.key.append(key)
    mac_sec_keychains.mac_sec_keychain.append(mac_sec_keychain)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    mac_sec_keychains = xr_lib_keychain_macsec_cfg.MacSecKeychains()  # create object
    config_mac_sec_keychains(mac_sec_keychains)  # add object configuration

    # encode and print object
    print(codec.encode(provider, mac_sec_keychains))

    exit()
# End of script
