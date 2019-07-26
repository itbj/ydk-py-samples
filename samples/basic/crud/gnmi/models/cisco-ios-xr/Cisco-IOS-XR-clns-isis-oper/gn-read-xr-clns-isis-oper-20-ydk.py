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

usage: nc-read-xr-clns-isis-oper-20-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_clns_isis_oper \
    as xr_clns_isis_oper
import re
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def process_isis(isis):
    """Process data in isis object."""
    # format string for isis neighbor header
    isis_header = ("IS-IS {instance} neighbors:\n"
                   "System Id      Interface        SNPA           State "
                   "Holdtime Type IETF-NSF")
    # format string for isis neighbor row
    isis_row = ("{sys_id:<14} {intf:<16} {snpa:<14} {state:<5} "
                "{hold:<8} {type_:<4} {ietf_nsf:^8}")
    # format string for isis neighbor trailer
    isis_trailer = "Total neighbor count: {count}"

    nbr_state = {0: "Up", 1: "Init", 2: "Fail"}
    nbr_type = {0: "None", 1: "L1", 2: "L2", 3: "L1L2"}

    if isis.instances.instance:
        show_isis_nbr = str()
    else:
        show_isis_nbr = "No IS-IS instances found"

    # iterate over all instances
    for instance in isis.instances.instance:
        if show_isis_nbr:
            show_isis_nbr += "\n\n"

        show_isis_nbr += isis_header.format(instance=instance.instance_name)
        nbr_count = 0
        host_name = instance.host_names.host_name
        host_names = dict([(h.system_id, h.host_name) for h in host_name])
        # iterate over all neighbors
        for neighbor in instance.neighbors.neighbor:
            nbr_count += 1
            sys_id = host_names[neighbor.system_id]
            intf = (neighbor.interface_name[:2] +
                    re.sub(r'\D+', "", neighbor.interface_name, 1))
            state = nbr_state[neighbor.neighbor_state.value]
            type_ = nbr_type[neighbor.neighbor_circuit_type.value]
            ietf_nsf = "Y" if neighbor.neighbor_ietf_nsf_capable_flag else "N"
            show_isis_nbr += ("\n" +
                              isis_row.format(sys_id=sys_id,
                                              intf=intf,
                                              snpa=neighbor.neighbor_snpa,
                                              state=state,
                                              hold=neighbor.neighbor_holdtime,
                                              type_=type_,
                                              ietf_nsf=ietf_nsf))
        if nbr_count:
            show_isis_nbr += "\n\n" + isis_trailer.format(count=nbr_count)

    # return formatted string
    return(show_isis_nbr)


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

    isis = xr_clns_isis_oper.Isis()  # create object

    # read data from gNMI device
    isis = crud.read(provider, isis)
    print(process_isis(isis))  # process object data

    exit()
# End of script
