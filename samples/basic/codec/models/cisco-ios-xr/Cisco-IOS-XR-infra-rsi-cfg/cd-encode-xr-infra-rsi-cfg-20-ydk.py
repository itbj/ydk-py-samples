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
Encode configuration for model Cisco-IOS-XR-infra-rsi-cfg.

usage: cd-encode-xr-infra-rsi-cfg-20-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_rsi_cfg \
    as xr_infra_rsi_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_cfg \
    as xr_ipv4_bgp_cfg
from ydk.types import Empty
import logging


def config_vrfs(vrfs):
    """Add config data to vrfs object."""
    # vrf RED
    vrf = vrfs.Vrf()
    vrf.vrf_name = "RED"
    vrf.create = Empty()

    # ipv4 unicast address family
    af = vrf.afs.Af()
    af.af_name = xr_infra_rsi_cfg.VrfAddressFamily.ipv4
    af.saf_name = xr_infra_rsi_cfg.VrfSubAddressFamily.unicast
    af.topology_name = "default"
    af.create = Empty()

    # import route targets
    route_target = af.bgp.import_route_targets.route_targets.RouteTarget()
    route_target.type = xr_ipv4_bgp_cfg.BgpVrfRouteTarget.as_
    as_or_four_byte_as = route_target.AsOrFourByteAs()
    as_or_four_byte_as.as_xx = 0
    as_or_four_byte_as.as_ = 65172
    as_or_four_byte_as.as_index = 1
    as_or_four_byte_as.stitching_rt = 0
    route_target.as_or_four_byte_as.append(as_or_four_byte_as)
    af.bgp.import_route_targets.route_targets.route_target.append(route_target)

    # export route targets
    route_target = af.bgp.export_route_targets.route_targets.RouteTarget()
    route_target.type = xr_ipv4_bgp_cfg.BgpVrfRouteTarget.as_
    as_or_four_byte_as = route_target.AsOrFourByteAs()
    as_or_four_byte_as.as_xx = 0
    as_or_four_byte_as.as_ = 65172
    as_or_four_byte_as.as_index = 1
    as_or_four_byte_as.stitching_rt = 0
    route_target.as_or_four_byte_as.append(as_or_four_byte_as)
    af.bgp.export_route_targets.route_targets.route_target.append(route_target)

    # append address family and vrf
    vrf.afs.af.append(af)
    vrfs.vrf.append(vrf)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    vrfs = xr_infra_rsi_cfg.Vrfs()  # create object
    config_vrfs(vrfs)  # add object configuration

    # encode and print object
    print(codec.encode(provider, vrfs))

    exit()
# End of script
