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
Execute RPC for model Cisco-IOS-XR-ping-act.

usage: nc-execute-xr-ping-act-20-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import ExecutorService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ping_act \
    as xr_ping_act
import logging


def prepare_ping_rpc(ping_rpc):
    """Add RPC input data to ping_rpc object."""
    ping_rpc.input.destination.destination = "10.0.0.1"


def process_ping_rpc(ping_rpc):
    """Process data in RPC output object."""
    # format string for reply header
    ping_reply_header = ('Sending 5, 100-byte ICMP Echos to {destination}, '
                         'timeout is 2 seconds:\n')
    # format string for reply trailer
    ping_reply_trailer = ('\nSuccess rate is {success_rate} percent '
                          '({hits}/{total}), '
                          'round-trip min/avg/max = {rtt_min}/{rtt_avg}/{rtt_max} ms')

    ping_response = ping_rpc.output.ping_response

    ping_reply = ping_reply_header.format(destination=ping_response.ipv4[0].destination)

    # iterate over all replies
    for reply in ping_response.ipv4[0].replies.reply:
        ping_reply += reply.result

    ping_reply += ping_reply_trailer.format(success_rate=ping_response.ipv4[0].success_rate,
                                            hits=ping_response.ipv4[0].hits,
                                            total=ping_response.ipv4[0].total,
                                            rtt_min=ping_response.ipv4[0].rtt_min,
                                            rtt_avg=ping_response.ipv4[0].rtt_avg,
                                            rtt_max=ping_response.ipv4[0].rtt_max,
                                            )

    # return formated string
    return ping_reply


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
    # create executor service
    executor = ExecutorService()

    ping_rpc = xr_ping_act.PingRpc()  # create object
    prepare_ping_rpc(ping_rpc)  # add RPC input

    # execute RPC on NETCONF device
    ping_rpc.output = executor.execute_rpc(provider, ping_rpc)
    print(process_ping_rpc(ping_rpc))

    exit()
# End of script
