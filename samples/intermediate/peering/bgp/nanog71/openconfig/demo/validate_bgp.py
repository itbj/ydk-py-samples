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

usage: validate_bgp.py [-h] [-v] node neighbor server

positional arguments:
  node           node streaming interface status
  neighbor       neighbor address
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
NEIGHBOR_SESSION_STATE = "ESTABLISHED"
TIMEOUT = 30


def validate_bgp(kafka_consumer, node, nbr_address,
                 session_state=NEIGHBOR_SESSION_STATE,
                 timeout=30):
    """Validate BGP session state."""
    telemetry_encoding_path = "openconfig-bgp:bgp/neighbors"
    start_time = time.time()
    for kafka_msg in kafka_consumer:
        msg = json.loads(kafka_msg.value)
        if (msg["Telemetry"]["node_id_str"] == node and
                msg["Telemetry"]["encoding_path"] == telemetry_encoding_path
                and "Rows" in msg):
            for row in msg["Rows"]:
                if "neighbor" in row["Content"]:
                    current_session_state = (row["Content"]["neighbor"]
                                                ["state"]["session-state"])
                    # return if bgp session in expected state
                    if (row["Content"]["neighbor"]
                           ["neighbor-address"] == nbr_address
                            and current_session_state == session_state):
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
                        help="node streaming interface status")
    parser.add_argument("neighbor",
                        help="neighbor address")
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

    print validate_bgp(kafka_consumer, args.node, args.neighbor)

    exit()
# End of script
