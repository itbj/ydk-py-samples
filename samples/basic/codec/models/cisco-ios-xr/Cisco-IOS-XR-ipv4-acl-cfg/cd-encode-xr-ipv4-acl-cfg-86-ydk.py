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
Encode configuration for model Cisco-IOS-XR-ipv4-acl-cfg.

usage: cd-encode-xr-ipv4-acl-cfg-86-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_cfg \
    as xr_ipv4_acl_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_datatypes \
    as xr_ipv4_acl_datatypes
from ydk.types import Empty
import logging


def config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list):
    """Add config data to ipv4_acl_and_prefix_list object."""
    prefix = ipv4_acl_and_prefix_list.prefixes.Prefix()
    prefix.prefix_list_name = "PREFIX-LIST4"
    prefix.prefix_list_entries = prefix.PrefixListEntries()

    # prefix list with sequence number 10
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 10
    prefix_list_entry.remark = "allow prefix ranges"
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)
    
    # prefix list with sequence number 20
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 20
    prefix_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnumEnum.permit
    prefix_list_entry.netmask = "255.255.0.0" 
    prefix_list_entry.prefix = "172.17.0.0"
    prefix_list_entry.min_prefix_length = 24
    prefix_list_entry.match_min_length = Empty()
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)

    # prefix list with sequence number 30
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 30
    prefix_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnumEnum.permit
    prefix_list_entry.netmask = "255.255.0.0" 
    prefix_list_entry.prefix = "172.18.0.0"
    prefix_list_entry.max_prefix_length = 24
    prefix_list_entry.match_max_length = Empty()
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)

    # prefix list with sequence number 40
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 40
    prefix_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnumEnum.permit
    prefix_list_entry.netmask = "255.255.0.0" 
    prefix_list_entry.prefix = "172.19.0.0"
    prefix_list_entry.max_prefix_length = 20
    prefix_list_entry.match_max_length = Empty()
    prefix_list_entry.min_prefix_length = 28
    prefix_list_entry.match_min_length = Empty()
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)
    ipv4_acl_and_prefix_list.prefixes.prefix.append(prefix)


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

    ipv4_acl_and_prefix_list = xr_ipv4_acl_cfg.Ipv4AclAndPrefixList()  # create object
    config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list)  # add object configuration

    # encode and print object
    print(codec.encode(provider, ipv4_acl_and_prefix_list))

    exit()
# End of script
