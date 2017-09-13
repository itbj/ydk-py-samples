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
Encode configuration for model openconfig-telemetry.

usage: cd-encode-oc-telemetry-32-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.openconfig import openconfig_telemetry \
    as oc_telemetry
import logging


def config_telemetry_system(telemetry_system):
    """Add config data to telemetry_system object."""
    #sensor-group
    sensor_group = telemetry_system.sensor_groups.SensorGroup()
    sensor_group.sensor_group_id = "SGROUP1"
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.path = "Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_system.sensor_groups.sensor_group.append(sensor_group)

    #subscription
    subscription = telemetry_system.subscriptions.persistent.Subscription()
    subscription.subscription_id = 1
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.config.sensor_group = "SGROUP1"
    sensor_profile.config.sample_interval = 30000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    telemetry_system.subscriptions.persistent.subscription.append(subscription)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    telemetry_system = oc_telemetry.TelemetrySystem()  # create object
    config_telemetry_system(telemetry_system)  # add object configuration

    # encode and print object
    print(codec.encode(provider, telemetry_system))

    exit()
# End of script
