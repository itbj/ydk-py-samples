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
Create configuration for model Cisco-IOS-XR-infra-syslog-cfg.

usage: nc-create-xr-infra-syslog-cfg-62-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_syslog_cfg \
    as xr_infra_syslog_cfg
from ydk.types import Empty
import logging


def config_syslog(syslog):
    """Add config data to syslog object."""
    #Rule Configuration
    rule = syslog.correlator.rules.Rule()
    rule.name = "RULE2"
    # rule.non_stateful.conext_correlation = Empty() <--this should give error but doesn't
    rule.non_stateful.timeout = 3600000
    rule.non_stateful.root_cause.category = "PLATFORM"
    rule.non_stateful.root_cause.group = "ENVMON"
    rule.non_stateful.root_cause.message_code = "FAN_FAIL"
    non_root_cause = rule.non_stateful.non_root_causes.NonRootCause()
    non_root_cause.category = "PLATFORM"
    non_root_cause.group = "ENVMON"
    non_root_cause.message_code = "FAN_CLEAR"
    rule.non_stateful.non_root_causes.non_root_cause.append(non_root_cause)
    non_root_cause = rule.non_stateful.non_root_causes.NonRootCause()
    non_root_cause.category = "PLATFORM"
    non_root_cause.group = "ENVMON"
    non_root_cause.message_code = "FANTRAY_FAIL"
    rule.non_stateful.non_root_causes.non_root_cause.append(non_root_cause)
    rule.non_stateful.timeout_root_cause = 360000
    rule.applied_to.all = Empty()
    syslog.correlator.rules.rule.append(rule)
    syslog.correlator.buffer_size = 65535


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

    syslog = xr_infra_syslog_cfg.Syslog()  # create object
    config_syslog(syslog)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, syslog)

    exit()
# End of script
