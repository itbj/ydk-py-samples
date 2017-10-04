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
Validate operation for model openconfig-interfaces.

usage: validate_interfaces.py [-h] [-v] node interface server

positional arguments:
  node           node streaming interface status
  interface      interface name
  server         kafka bootstrap server (host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

import kafka
import json
import time
import logging

from argparse import ArgumentParser

KAFKA_TOPIC = 'pipeline'
ADMIN_STATUS_UP = "UP"
TIMEOUT = 30


def validate_interfaces(kafka_consumer, node, if_name,
                        admin_status=ADMIN_STATUS_UP,
                        timeout=30):
    """Validate interface admin status."""
    telemetry_encoding_path = "openconfig-interfaces:interfaces/interface"
    start_time = time.time()
    for kafka_msg in kafka_consumer:
        msg = json.loads(kafka_msg.value)
        if (msg["Telemetry"]["node_id_str"] == node and
                msg["Telemetry"]["encoding_path"] == telemetry_encoding_path
                and "Rows" in msg):
            for row in msg["Rows"]:
                if "subinterfaces" in row["Content"]:
                    current_admin_status = (row["Content"]["subinterfaces"]
                                               ["subinterface"]["state"]
                                               ["admin-status"])
                    # return if intf in expected admin status
                    if (row["Keys"]["name"] == if_name
                            and current_admin_status == admin_status):
                        return True

        if time.time() - start_time > timeout:
            break

    return False


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("node",
                        help="node router streaming interface status")
    parser.add_argument("interface",
                        help="interface name")
    parser.add_argument("server",
                        help="kafka bootstrap server (host:port)")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("kafka")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create kafka consumer to pipeline topic
    kafka_consumer = kafka.KafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=args.server,
                                         consumer_timeout_ms=TIMEOUT*1000)

    print validate_interfaces(kafka_consumer, args.node, args.interface)

    exit()
# End of script
