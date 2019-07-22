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
Create configuration for model openconfig-acl.

usage: gn-create-oc-acl-30-ydk.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_acl \
    as oc_acl
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_acl(acl):
    """Add config data to acl object."""
    # acl-set configuration
    acl_set = acl.AclSets.AclSet()
    acl_set.name = "ACL1"
    acl_set.type = oc_acl.ACLIPV4()
    acl_set.config.name = "ACL1"
    acl_set.config.type = oc_acl.ACLIPV4()
    acl_set.acl_entries = acl_set.AclEntries()

    # acl-entry with sequence number 10
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 10
    acl_entry.config.sequence_id = 10
    acl_set.acl_entries.acl_entry.append(acl_entry)

    # acl-entry with sequence number 20
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 20
    acl_entry.config.sequence_id = 20
    acl_entry.actions.config.forwarding_action = oc_acl.ACCEPT()
    acl_entry.ipv4.config.source_address = "172.31.255.1/32"
    acl_set.acl_entries.acl_entry.append(acl_entry)

    # acl-entry with sequence number 30
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 30
    acl_entry.config.sequence_id = 30
    acl_entry.actions.config.forwarding_action = oc_acl.REJECT()
    acl_set.acl_entries.acl_entry.append(acl_entry)
    acl.acl_sets.acl_set.append(acl_set)


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

    acl = oc_acl.Acl()  # create object
    config_acl(acl)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, acl)

    exit()
# End of script
