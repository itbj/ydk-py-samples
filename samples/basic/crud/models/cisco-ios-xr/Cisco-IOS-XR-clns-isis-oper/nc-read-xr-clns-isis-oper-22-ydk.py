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
Read all data for model Cisco-IOS-XR-clns-isis-oper.

usage: nc-read-xr-clns-isis-oper-22-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_clns_isis_oper \
    as xr_clns_isis_oper
from datetime import timedelta
import re
import logging


def process_isis(isis):
    """Process data in isis object."""
    # format string for isis adjacency header
    isis_header = ("IS-IS {instance} Level-{level} adjacencies:\n"
                   "System Id      Interface        SNPA           State "
                   "Hold Changed  NSF IPv4 IPv6\n"
                   "                                                    "
                   "                   BFD  BFD")

    # format string for isis adjacency row
    isis_row = ("{sys_id:<14} {intf:<16} {snpa:<14} {state:<5} "
                "{hold:<4} {changed:<8} {ietf_nsf:<3} {v4_bfd:<4} {v6_bfd:<4}")
    # format string for isis adjacency trailer
    isis_trailer = "Total adjacency count: {count}"

    adj_state = {0: "Up", 1: "Init", 2: "Fail"}
    adj_bfd_state = {0: "None", 1: "Down", 2: "Init", 3: "Up"}

    if isis.instances.instance:
        show_isis_adj = str()
    else:
        show_isis_adj = "No IS-IS instances found"

    # iterate over all instances
    for instance in isis.instances.instance:
        host_name = instance.host_names.host_name
        host_names = dict([(h.system_id, h.host_name) for h in host_name])

        # iterate over all levels
        for level in instance.levels.level:
            if show_isis_adj:
                show_isis_adj += "\n\n"

            show_isis_adj += isis_header.format(instance=instance.instance_name,
                                                level=level.level.value)
            adj_count = 0
            # iterate over all adjacencies
            for adjacency in level.adjacencies.adjacency:
                adj_count += 1
                sys_id = host_names[adjacency.adjacency_system_id]
                intf = (adjacency.adjacency_interface[:2] +
                        re.sub(r'\D+', "", adjacency.adjacency_interface, 1))
                snpa = adjacency.adjacency_snpa
                state = adj_state[adjacency.adjacency_state.value]
                hold = adjacency.adjacency_holdtime
                changed = str(timedelta(seconds=adjacency.adjacency_uptime))
                if adjacency.adjacency_ietf_nsf_capable_flag:
                    ietf_nsf = "Yes"
                else:
                    ietf_nsf = "No"
                v4_bfd = adj_bfd_state[adjacency.adjacency_ipv6bfd_state.value]
                v6_bfd = adj_bfd_state[adjacency.adjacency_bfd_state.value]

                show_isis_adj += ("\n" +
                                  isis_row.format(sys_id=sys_id,
                                                  intf=intf,
                                                  snpa=snpa,
                                                  state=state,
                                                  hold=hold,
                                                  changed=changed,
                                                  ietf_nsf=ietf_nsf,
                                                  v4_bfd=v4_bfd,
                                                  v6_bfd=v6_bfd))
            if adj_count:
                show_isis_adj += ("\n\n" +
                                  isis_trailer.format(count=adj_count))

    # return formatted string
    return(show_isis_adj)


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

    isis = xr_clns_isis_oper.Isis()  # create object

    # read data from NETCONF device
    isis = crud.read(provider, isis)
    print(process_isis(isis))  # process object data

    exit()
# End of script
