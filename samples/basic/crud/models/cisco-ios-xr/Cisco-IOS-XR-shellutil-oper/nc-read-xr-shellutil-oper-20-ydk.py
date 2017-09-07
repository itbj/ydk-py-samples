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
Read all data for model Cisco-IOS-XR-shellutil-oper.

usage: nc-read-xr-shellutil-oper-20-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper \
    as xr_shellutil_oper
import datetime
import textwrap
import logging


def process_system_time(system_time):
    """Process data in system_time object."""
    # format string for system time
    show_system_time = textwrap.dedent("""
        Host: {host}
        System time: {time} {tzone} {date}
        Time source: {source}
        System uptime: {uptime}
        """).strip()

    # create time object
    clock_time = datetime.time(system_time.clock.hour,
                               system_time.clock.minute,
                               system_time.clock.second,
                               system_time.clock.millisecond / 1000)

    # create date object
    clock_date = datetime.date(system_time.clock.year,
                               system_time.clock.month,
                               system_time.clock.day)

    # convert uptime from seconds
    clock_delta = datetime.timedelta(seconds=system_time.uptime.uptime)

    # return formatted string
    return(show_system_time.format(host=system_time.uptime.host_name,
                                   time=clock_time,
                                   tzone=system_time.clock.time_zone,
                                   date=clock_date,
                                   source=system_time.clock.time_source.name,
                                   uptime=clock_delta))


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

    system_time = xr_shellutil_oper.SystemTime()  # create object

    # read data from NETCONF device
    system_time = crud.read(provider, system_time)
    print(process_system_time(system_time))  # process object data

    exit()
# End of script
