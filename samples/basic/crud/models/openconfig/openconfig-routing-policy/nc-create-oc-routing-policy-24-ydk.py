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
Create configuration for model openconfig-routing-policy.

usage: nc-create-oc-routing-policy-24-ydk.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_routing_policy \
    as oc_routing_policy
from ydk.models.openconfig import openconfig_policy_types \
    as oc_policy_types
from ydk.types import Empty
import logging


def config_routing_policy(routing_policy):
    """Add config data to routing_policy object."""
    # configure as-path set
    bgp_defined_sets = routing_policy.defined_sets.bgp_defined_sets
    as_path_set = bgp_defined_sets.as_path_sets.AsPathSet()
    as_path_set.as_path_set_name = "AS-PATH-SET1"
    as_path_set.as_path_set_member.append("^65172")
    bgp_defined_sets.as_path_sets.as_path_set.append(as_path_set)

    # configure community set
    bgp_defined_sets = routing_policy.defined_sets.bgp_defined_sets
    community_set = bgp_defined_sets.community_sets.CommunitySet()
    community_set.community_set_name = "COMMUNITY-SET1"
    community_set.community_member.append("ios-regex '^65172:17...$'")
    community_set.community_member.append("65172:16001")
    bgp_defined_sets.community_sets.community_set.append(community_set)

    # configure policy definition
    policy_definition = routing_policy.policy_definitions.PolicyDefinition()
    policy_definition.name = "POLICY2"
    # community-set statement
    statement = policy_definition.statements.Statement()
    statement.name = "community-set1"
    bgp_conditions = statement.conditions.bgp_conditions
    match_community_set = bgp_conditions.MatchCommunitySet()
    match_community_set.community_set = "COMMUNITY-SET1"
    match_set_options = oc_policy_types.MatchSetOptionsType.ALL
    match_community_set.match_set_options = match_set_options
    bgp_conditions.match_community_set = match_community_set
    statement.actions.accept_route = Empty()
    policy_definition.statements.statement.append(statement)
    # as-path-set statement
    statement = policy_definition.statements.Statement()
    statement.name = "as-path-set1"
    bgp_conditions = statement.conditions.bgp_conditions
    match_as_path_set = bgp_conditions.MatchAsPathSet()
    match_as_path_set.as_path_set = "AS-PATH-SET1"
    match_set_options = oc_policy_types.MatchSetOptionsType.ANY
    match_as_path_set.match_set_options = match_set_options
    bgp_conditions.match_as_path_set = match_as_path_set
    statement.actions.bgp_actions.set_local_pref = 50
    statement.actions.accept_route = Empty()
    policy_definition.statements.statement.append(statement)
    # reject statement
    statement = policy_definition.statements.Statement()
    statement.name = "reject route"
    statement.actions.reject_route = Empty()
    policy_definition.statements.statement.append(statement)

    routing_policy.policy_definitions.policy_definition.append(policy_definition)


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
        logger.setLevel(logging.DEBUG)
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

    routing_policy = oc_routing_policy.RoutingPolicy()  # create object
    config_routing_policy(routing_policy)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, routing_policy)

    exit()
# End of script
