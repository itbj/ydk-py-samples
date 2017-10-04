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

"""
Deploy a validated BGP peer using OpenConfig models.

usage: deploy_peer.py [-h] [-v] config

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser

import kafka
import sys
import json
import datetime

from config_interfaces import config_interfaces
from validate_interfaces import validate_interfaces
from config_bgp import config_bgp
from validate_bgp import validate_bgp

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.openconfig import openconfig_interfaces as oc_interfaces
from ydk.models.openconfig import openconfig_bgp as oc_bgp
import logging

KAFKA_TOPIC = 'pipeline'
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
KAFKA_TIMEOUT = 30

VALIDATE_TIMEOUT = 45

username = password = "admin"

sys.dont_write_bytecode = True

def validate_msg(status):
    OK = '\033[92m OK \033[0m'
    FAIL = '\033[91mFAIL\033[0m'
    if status:
        return OK
    else:
        return FAIL


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("peer_config_file_name",
                        help="peer configuration file (JSON)")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        ydk_logger = logging.getLogger("ydk")
        ydk_logger.setLevel(logging.DEBUG)
        kafka_logger = logging.getLogger("kafka")
        kafka_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        ydk_logger.addHandler(handler)
        kafka_logger.addHandler(handler)

    # load peer configuration file (JSON)
    print("{}: Loading peer configuration .... ".format(datetime.datetime.now())),
    sys.stdout.flush()
    with open(args.peer_config_file_name) as peer_config_file:
        peer_config = json.load(peer_config_file)
    print("[{}]".format(validate_msg(True)))

    print("{}: Configure interface ........... ".format(datetime.datetime.now())),
    sys.stdout.flush()
    # connect to asbr
    provider = NetconfServiceProvider(address=peer_config["asbr"]["address"],
                                      username=username,
                                      password=password)

    # create CRUD service
    crud = CRUDService()

    # create kafka consumer to pipeline topic
    kafka_consumer = kafka.KafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                                         consumer_timeout_ms=KAFKA_TIMEOUT*1000)

    interfaces = oc_interfaces.Interfaces()
    config_interfaces(interfaces,
                      name=peer_config["interface"]["name"].encode("utf-8"),
                      description=peer_config["interface"]["description"].encode("utf-8"),
                      address_ip=peer_config["interface"]["address"].encode("utf-8"),
                      prefix_length=peer_config["interface"]["netmask"])
    crud.create(provider, interfaces)
    if_status = validate_interfaces(kafka_consumer,
                                    peer_config["asbr"]["name"],
                                    peer_config["interface"]["name"],
                                    timeout=VALIDATE_TIMEOUT)
    print("[{}]".format(validate_msg(if_status)))

    if if_status:
        print("{}: Configure BGP ................. ".format(datetime.datetime.now())),
        sys.stdout.flush()
        bgp = oc_bgp.Bgp()
        config_bgp(bgp,
                   local_as=peer_config["as"],
                   nbr_address=peer_config["neighbor"]["address"].encode("utf-8"),
                   nbr_as=peer_config["neighbor"]["as"])
        crud.create(provider, bgp)
        nbr_status = validate_bgp(kafka_consumer,
                                  peer_config["asbr"]["name"],
                                  peer_config["neighbor"]["address"],
                                  timeout=VALIDATE_TIMEOUT)
        print("[{}]".format(validate_msg(nbr_status)))

    sys.exit()
# End of script
