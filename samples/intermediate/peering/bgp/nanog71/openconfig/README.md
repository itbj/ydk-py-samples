# Getting Started with OpenConfig
This demostration illustrates a basic BGP peer deployment using OpenConfig data models.  Configuration changes are made using YDK.  State validation is performed using operational state that the network device streams using telemetry.  A modified version of the YDK Vagrant sandbox provides the YDK installation, the telemetry collector (Pipeline) and the message bus (Kafka) for state validation.

## Recommended Demo Execution
The `demo` directory is shared between your host and the Vagrant box.  The instructions below assume that the directory where the Vagrantfile resides is your current working directory.

1. Bring up the Vagrant box
```
$ vagrant up
```

2. Connect to the Vagrant box and change your current path to the `demo` directory
```
$ vagrant ssh
vagrant@nanog71-oc:~$ cd demo
vagrant@nanog71-oc:demo$
```

3. Configure the routing policy on ASBR1
```
vagrant@nanog71-oc:demo$ ./config_routing_policy.py ssh://user:password@host:port
vagrant@nanog71-oc:demo$
```

4. From a second shell, bring up another connection to your Vagrant box and execute the script for dumping your telemetry messages
```
$ vagrant ssh
vagrant@nanog71-oc:~$ demo/consume_telemetry.py
```

5. On your initial shell, configure telemetry on ASBR1
```
vagrant@nanog71-oc:demo$ ./config_telemetry.py ssh://user:password@host:port
vagrant@nanog71-oc:demo$
```
Depending on your network latency, your consumer script should start printing telemetry records between 20-40s later.

6. Deploy peer configuration as defined in `peer.json`
```
nog71-oc:demo$ more peer.json
{
    "asbr": {
        "name": "asbr1",
        "address": "198.18.1.11"
    },
    "as": 65001,
    "interface": {
        "name": "GigabitEthernet0/0/0/0",
        "description": "Peering with AS65002",
        "address": "192.168.0.1",
        "netmask": 24
    },
    "neighbor": {
        "address": "192.168.0.2",
        "as": 65002
    }
}
vagrant@nanog71-oc:demo$
vagrant@nanog71-oc:demo$ ./deploy_peer.py peer.json
2017-10-03 16:18:07.265978: Loading peer configuration ....  [ OK ]
2017-10-03 16:18:07.266935: Configure interface ...........  [ OK ]
2017-10-03 16:18:15.137814: Configure BGP .................  [ OK ]
vagrant@nanog71-oc:demo$
```

Note that all scripts support a `-v/--verbose` option to enable logging.

## Demo Ingredients
The demo is self-contained using the Vagrant box and interacting with Cisco XRv9K routers running Cisco IOS XR 6.2.1.

### Data Models
* openconfig-routing-policy 1.1.0
* openconfig-telemetry 0.2.0
* openconfig-interfaces 0.2.0
* openconfig-bgp 1.1.0

### SDK
YDK 0.5.5

### Telemetry and messaging tools
* Pipeline 1.0.0
* Kafka 0.10.0.0
* zookeeper 3.4.6
