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

usage: cd-encode-xr-policy-repository-cfg-26-ydk.py [-h] [-v]

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
    set_name = "PREFIX-SET1"
    rpl_prefix_set = """
        prefix-set PREFIX-SET1
          10.0.0.0/16 ge 24 le 32,
          172.0.0.0/8 ge 16 le 32
        end-set
        """
    community_set_name = "COMMUNITY-SET2"
    rpl_community_set = """
        community-set COMMUNITY-SET2
          65172:17001
        end-set
        """
    route_policy_name = "POLICY3"
    rpl_route_policy = """
        route-policy POLICY3
          #statement-name prefix-set1
          if destination in PREFIX-SET1 then
            set local-preference 1000
            set community COMMUNITY-SET2
            done
          endif
          #statement-name reject
          drop
        end-policy
        """
    # configure prefix set
    prefix_set = routing_policy.sets.prefix_sets.PrefixSet()
    prefix_set.set_name = set_name
    prefix_set.rpl_prefix_set = rpl_prefix_set
    routing_policy.sets.prefix_sets.prefix_set.append(prefix_set)

    # configure community set
    community_set = routing_policy.sets.community_sets.CommunitySet()
    community_set.set_name = community_set_name
    community_set.rpl_community_set = rpl_community_set
    routing_policy.sets.community_sets.community_set.append(community_set)

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
