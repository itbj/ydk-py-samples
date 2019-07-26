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

usage: gn-create-oc-routing-policy-26-ydk.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_routing_policy \
    as oc_routing_policy
from ydk.models.openconfig import openconfig_policy_types \
    as oc_policy_types
from ydk.models.openconfig import openconfig_bgp_policy \
    as oc_bgp_policy
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_routing_policy(routing_policy):
    """Add config data to routing_policy object."""
    # configure prefix set
    prefix_set = routing_policy.defined_sets.prefix_sets.PrefixSet()
    prefix_set.prefix_set_name = "PREFIX-SET1"
    prefix_set.config.prefix_set_name = "PREFIX-SET1"
    prefix = prefix_set.prefixes.Prefix()
    prefix.ip_prefix = "10.0.0.0/16"
    prefix.masklength_range = "24..32"
    prefix.config.ip_prefix = "10.0.0.0/16"
    prefix.config.masklength_range = "24..32"
    prefix_set.prefixes.prefix.append(prefix)
    prefix = prefix_set.prefixes.Prefix()
    prefix.ip_prefix = "172.0.0.0/8"
    prefix.masklength_range = "16..32"
    prefix.config.ip_prefix = "172.0.0.0/8"
    prefix.config.masklength_range = "16..32"
    prefix_set.prefixes.prefix.append(prefix)
    routing_policy.defined_sets.prefix_sets.prefix_set.append(prefix_set)

    # configure community set
    bgp_defined_sets = routing_policy.defined_sets.bgp_defined_sets
    community_set = bgp_defined_sets.community_sets.CommunitySet()
    community_set.community_set_name = "COMMUNITY-SET2"
    community_set.config.community_set_name = "COMMUNITY-SET2"
    community_set.config.community_member.append("65172:17001")
    bgp_defined_sets.community_sets.community_set.append(community_set)

    # configure policy definition
    policy_definition = routing_policy.policy_definitions.PolicyDefinition()
    policy_definition.name = "POLICY3"
    policy_definition.config.name = "POLICY3"
    # prefix-set statement
    statement = policy_definition.statements.Statement()
    statement.name = "prefix-set1"
    statement.config.name = "prefix-set1"
    match_prefix_set = statement.conditions.MatchPrefixSet()
    match_prefix_set.config.prefix_set = "PREFIX-SET1"
    match_set_options = oc_policy_types.MatchSetOptionsRestrictedType.ANY
    match_prefix_set.config.match_set_options = match_set_options
    statement.conditions.match_prefix_set = match_prefix_set
    statement.actions.bgp_actions.config.set_local_pref = 1000
    set_community = statement.actions.bgp_actions.SetCommunity()
    set_community.reference.config.community_set_ref = "COMMUNITY-SET2"
    set_community.config.options = oc_bgp_policy.BgpSetCommunityOptionType.REPLACE
    statement.actions.bgp_actions.set_community = set_community
    statement.actions.config.accept_route = Empty()
    policy_definition.statements.statement.append(statement)
    # reject statement
    statement = policy_definition.statements.Statement()
    statement.name = "reject"
    statement.config.name = "reject"
    statement.actions.config.reject_route = Empty()
    policy_definition.statements.statement.append(statement)

    routing_policy.policy_definitions.policy_definition.append(policy_definition)


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

    routing_policy = oc_routing_policy.RoutingPolicy()  # create object
    config_routing_policy(routing_policy)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, routing_policy)

    exit()
# End of script
