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
Encode configuration for model Cisco-IOS-XR-aaa-lib-cfg.

usage: cd-encode-xr-aaa-lib-cfg-22-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_aaa_lib_cfg \
    as xr_aaa_lib_cfg
import logging


def config_aaa(aaa):
    """Add config data to aaa object."""
    username = aaa.usernames.Username()
    username.ordering_index = 22
    username.name = "netop"
    username.secret = "$1$Z/8E$GDBQs1PtqJnwlQ9kKGpXj/"
    # task group
    usergroup_under_username = username.usergroup_under_usernames.UsergroupUnderUsername()
    usergroup_under_username.name = "netadmin"
    username.usergroup_under_usernames.usergroup_under_username.append(usergroup_under_username)
    # task group
    usergroup_under_username = username.usergroup_under_usernames.UsergroupUnderUsername()
    usergroup_under_username.name = "operator"
    username.usergroup_under_usernames.usergroup_under_username.append(usergroup_under_username)
    aaa.usernames.username.append(username)


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

    aaa = xr_aaa_lib_cfg.Aaa()  # create object
    config_aaa(aaa)  # add object configuration

    # encode and print object
    print(codec.encode(provider, aaa))

    exit()
# End of script
