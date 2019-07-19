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
Encode configuration for model Cisco-IOS-XR-segment-routing-ms-cfg.

usage: cd-encode-xr-segment-routing-ms-cfg-21-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg \
    as xr_segment_routing_ms_cfg
import logging


def config_sr(sr):
    """Add config data to sr object."""
    mapping = sr.mappings.Mapping()
    mapping.af = xr_segment_routing_ms_cfg.SrmsAddressFamily.ipv6
    mapping.ip = "2001:db8::ff:1"
    mapping.mask = 128
    mapping.sid_start = 4061
    mapping.sid_range = 1
    sr.mappings.mapping.append(mapping)


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

    sr = xr_segment_routing_ms_cfg.Sr()  # create object
    config_sr(sr)  # add object configuration

    # encode and print object
    print(codec.encode(provider, sr))

    exit()
# End of script
