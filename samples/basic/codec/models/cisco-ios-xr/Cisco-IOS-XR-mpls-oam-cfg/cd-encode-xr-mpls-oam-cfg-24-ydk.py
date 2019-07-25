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
Create configuration for model Cisco-IOS-XR-mpls-oam-cfg.

usage: cd-encode-xr-mpls-oam-cfg-24-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_mpls_oam_cfg \
    as xr_mpls_oam_cfg
from ydk.types import Empty
import logging


def config_mpls_oam(mpls_oam):
    """Add config data to mpls_oam object."""
    mpls_oam.enable_oam = Empty()
    mpls_oam.disable_vendor_extension = Empty()
    mpls_oam.reply_mode.control_channel.allow_reverse_lsp = Empty()


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

    # create CRUD service
    codec = CodecService()

    mpls_oam = xr_mpls_oam_cfg.MplsOam()  # create object
    config_mpls_oam(mpls_oam)  # add object configuration

    # encode and print object
    print(codec.encode(provider, mpls_oam))

    exit()
# End of script
