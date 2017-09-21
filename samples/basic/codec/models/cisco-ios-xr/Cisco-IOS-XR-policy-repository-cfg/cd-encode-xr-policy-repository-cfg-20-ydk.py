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
Encode configuration for model Cisco-IOS-XR-policy-repository-cfg.

usage: cd-encode-xr-policy-repository-cfg-20-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_policy_repository_cfg \
    as xr_policy_repository_cfg
import logging


def config_routing_policy(routing_policy):
    """Add config data to routing_policy object."""
    route_policy_name = "PASS-ALL"
    rpl_route_policy = """
        route-policy PASS-ALL
          #statement-name pass-all
          pass
        end-policy
        """
    # configure RPL policy
    route_policy = routing_policy.route_policies.RoutePolicy()
    route_policy.route_policy_name = route_policy_name
    route_policy.rpl_route_policy = rpl_route_policy
    routing_policy.route_policies.route_policy.append(route_policy)


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

    routing_policy = xr_policy_repository_cfg.RoutingPolicy()  # create object
    config_routing_policy(routing_policy)  # add object configuration

    # encode and print object
    print(codec.encode(provider, routing_policy))

    exit()
# End of script
