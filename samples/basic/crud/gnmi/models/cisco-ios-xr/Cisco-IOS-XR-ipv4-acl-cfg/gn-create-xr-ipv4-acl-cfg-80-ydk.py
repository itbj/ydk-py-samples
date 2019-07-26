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
Create configuration for model Cisco-IOS-XR-ipv4-acl-cfg.

usage: gn-create-xr-ipv4-acl-cfg-80-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_cfg \
    as xr_ipv4_acl_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_datatypes \
    as xr_ipv4_acl_datatypes
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list):
    """Add config data to ipv4_acl_and_prefix_list object."""
    prefix = ipv4_acl_and_prefix_list.prefixes.Prefix()
    prefix.prefix_list_name = "PREFIX-LIST1"
    prefix.prefix_list_entries = prefix.PrefixListEntries()

    # prefix list with sequence number 10
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 10
    prefix_list_entry.remark = "allow single prefix"
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)
    
    # prefix list with sequence number 20
    prefix_list_entry = prefix.prefix_list_entries.PrefixListEntry()
    prefix_list_entry.sequence_number = 20
    prefix_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnum.permit
    prefix_list_entry.netmask = "255.255.0.0"
    prefix_list_entry.prefix = "172.16.0.0"
    prefix.prefix_list_entries.prefix_list_entry.append(prefix_list_entry)
    ipv4_acl_and_prefix_list.prefixes.prefix.append(prefix)


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

    ipv4_acl_and_prefix_list = xr_ipv4_acl_cfg.Ipv4AclAndPrefixList()  # create object
    config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, ipv4_acl_and_prefix_list)

    exit()
# End of script
