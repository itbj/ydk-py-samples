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
Create configuration for model Cisco-IOS-XR-policy-repository-cfg.

usage: nc-create-xr-policy-repository-cfg-24-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_policy_repository_cfg \
    as xr_policy_repository_cfg
import logging


def config_routing_policy(routing_policy):
    """Add config data to routing_policy object."""
    community_set_name = "COMMUNITY-SET1"
    rpl_community_set = """
        community-set COMMUNITY-SET1
          ios-regex '^65172:17...$',
          65172:16001
        end-set
        """
    as_path_set_name = "AS-PATH-SET1"
    rplas_path_set = """
        as-path-set AS-PATH-SET1
          ios-regex '^65172'
        end-set
        """
    route_policy_name = "POLICY2"
    rpl_route_policy = """
        route-policy POLICY2
          #statement-name community-set1
          if community matches-every COMMUNITY-SET1 then
            done
          endif
          #statement-name as-path-set1
          if as-path in AS-PATH-SET1 then
            set local-preference 50
            done
          endif
          #statement-name reject route
          drop
        end-policy
        """
    # configure community set
    community_set = routing_policy.sets.community_sets.CommunitySet()
    community_set.set_name = community_set_name
    community_set.rpl_community_set = rpl_community_set
    routing_policy.sets.community_sets.community_set.append(community_set)

    # configure as-path set
    as_path_set = routing_policy.sets.as_path_sets.AsPathSet()
    as_path_set.set_name = as_path_set_name
    as_path_set.rplas_path_set = rplas_path_set
    routing_policy.sets.as_path_sets.as_path_set.append(as_path_set)

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

    routing_policy = xr_policy_repository_cfg.RoutingPolicy()  # create object
    config_routing_policy(routing_policy)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, routing_policy)

    exit()
# End of script
