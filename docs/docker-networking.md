Get started

## Networking overview

Container networking refers to the ability for containers to connect to and
communicate with each other, and with non-Docker network services.
Containers have networking enabled by default, and they can make outgoing
connections. A container has no information about what kind of network it's
attached to, or whether its network peers are also Docker containers. A
container only sees a network interface with an IP address, a gateway, a
routing table, DNS services, and other networking details.
This page describes networking from the point of view of the container,
and the concepts around container networking.
When Docker Engine on Linux starts for the first time, it has a single
built-in network called the "default bridge" network. When you run a
container without the--networkoption, it is connected to the default
bridge.
Containers attached to the default bridge have access to network services
outside the Docker host. They use "masquerading" which means, if the
Docker host has Internet access, no additional configuration is needed
for the container to have Internet access.
For example, to run a container on the default bridge network, and have
it ping an Internet host:
`$docker run --rm -ti busybox ping -c1 docker.comPING docker.com (23.185.0.4): 56 data bytes64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms--- docker.com ping statistics ---1 packets transmitted, 1 packets received, 0% packet lossround-trip min/avg/max = 6.564/6.564/6.564 ms`
`$docker run --rm -ti busybox ping -c1 docker.comPING docker.com (23.185.0.4): 56 data bytes64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms--- docker.com ping statistics ---1 packets transmitted, 1 packets received, 0% packet lossround-trip min/avg/max = 6.564/6.564/6.564 ms`

## User-defined networks

With the default configuration, containers attached to the default
bridge network have unrestricted network access to each other using
container IP addresses. They cannot refer to each other by name.
It can be useful to separate groups of containers that should have full
access to each other, but restricted access to containers in other groups.
You can create custom, user-defined networks, and connect groups of containers
to the same network. Once connected to a user-defined network, containers
can communicate with each other using container IP addresses or container names.
The following example creates a network using thebridgenetwork driver and
runs a container in that network:
`$docker network create -d bridge my-net$docker run --network=my-net -it busybox`
`$docker network create -d bridge my-net$docker run --network=my-net -it busybox`
Docker Engine has a number of network drivers, as well as the default "bridge".
On Linux, the following built-in network drivers are available:
More information can be found in the network driver specific pages, including
their configuration options and details about their functionality.
Native Windows containers have a different set of drivers, seeWindows container network drivers.

## Connecting to multiple networks

Connecting a container to a network can be compared to connecting an Ethernet
cable to a physical host. Just as a host can be connected to multiple Ethernet
networks, a container can be connected to multiple Docker networks.
For example, a frontend container may be connected to a bridge network
with external access, and a--internalnetwork
to communicate with containers running backend services that do not need
external network access.
A container may also be connected to different types of network. For example,
anipvlannetwork to provide internet access, and abridgenetwork for
access to local services.
Containers can also share networking stacks, seeContainer networks.
When sending packets, if the destination is an address in a directly connected
network, packets are sent to that network. Otherwise, packets are sent to
a default gateway for routing to their destination. In the example above,
theipvlannetwork's gateway must be the default gateway.
The default gateway is selected by Docker, and may change whenever a
container's network connections change.
To make Docker choose a specific default gateway when creating the container
or connecting a new network, set a gateway priority. See optiongw-priorityfor thedocker runanddocker network connectcommands.
`gw-priority`
`docker network connect`
The defaultgw-priorityis0and the gateway in the network with the
highest priority is the default gateway. So, when a network should always
be the default gateway, it is enough to set itsgw-priorityto1.
`gw-priority`
`gw-priority`
`$docker run --networkname=gwnet,gw-priority=1--network anet1 --name myctr myimage$docker network connect anet2 myctr`
`$docker run --networkname=gwnet,gw-priority=1--network anet1 --name myctr myimage$docker network connect anet2 myctr`

## Published ports

When you create or run a container usingdocker createordocker run, all
ports of containers on bridge networks are accessible from the Docker host and
other containers connected to the same network. Ports are not accessible from
outside the host or, with the default configuration, from containers in other
networks.
`docker create`
Use the--publishor-pflag to make a port available outside the host,
and to containers in other bridge networks.
For more information about port mapping, including how to disable it and use
direct routing to containers, seeport publishing.

## IP address and hostname

When creating a network, IPv4 address allocation is enabled by default, it
can be disabled using--ipv4=false. IPv6 address allocation can be enabled
using--ipv6.
`--ipv4=false`
`$docker network create --ipv6 --ipv4=falsev6net`
`$docker network create --ipv6 --ipv4=falsev6net`
By default, the container gets an IP address for every Docker network it attaches to.
A container receives an IP address out of the IP subnet of the network.
The Docker daemon performs dynamic subnetting and IP address allocation for containers.
Each network also has a default subnet mask and gateway.
You can connect a running container to multiple networks,
either by passing the--networkflag multiple times when creating the container,
or using thedocker network connectcommand for already running containers.
In both cases, you can use the--ipor--ip6flags to specify the container's IP address on that particular network.
`docker network connect`
In the same way, a container's hostname defaults to be the container's ID in Docker.
You can override the hostname using--hostname.
When connecting to an existing network usingdocker network connect,
you can use the--aliasflag to specify an additional network alias for the container on that network.
`docker network connect`

## Subnet allocation

Docker networks can use either explicitly configured subnets or automatically allocated ones from default pools.

## Explicit subnet configuration

You can specify exact subnets when creating a network:
`$docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet`
`$docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet`

## Automatic subnet allocation

When no--subnetoption is provided, Docker automatically selects a subnet from predefined "default address pools".
These pools can be configured in/etc/docker/daemon.json. Docker's built-in default is equivalent to:
`/etc/docker/daemon.json`
`{"default-address-pools":[{"base":"172.17.0.0/16","size":16},{"base":"172.18.0.0/16","size":16},{"base":"172.19.0.0/16","size":16},{"base":"172.20.0.0/14","size":16},{"base":"172.24.0.0/14","size":16},{"base":"172.28.0.0/14","size":16},{"base":"192.168.0.0/16","size":20}]}`
`{"default-address-pools":[{"base":"172.17.0.0/16","size":16},{"base":"172.18.0.0/16","size":16},{"base":"172.19.0.0/16","size":16},{"base":"172.20.0.0/14","size":16},{"base":"172.24.0.0/14","size":16},{"base":"172.28.0.0/14","size":16},{"base":"192.168.0.0/16","size":20}]}`
base: The subnet that can be allocated from.
size: The prefix length used for each allocated subnet.
When an IPv6 subnet is required and there are no IPv6 addresses indefault-address-pools, Docker allocates
subnets from a Unique Local Address (ULA) prefix. To use specific IPv6 subnets instead, add them to yourdefault-address-pools. SeeDynamic IPv6 subnet allocationfor more information.
`default-address-pools`
`default-address-pools`
Docker attempts to avoid address prefixes already in use on the host. However, you may need to customizedefault-address-poolsto prevent routing conflicts in some network environments.
`default-address-pools`
The default pools use large subnets, which limits the number of networks you can create. You can divide base
subnets into smaller pools to support more networks.
For example, this configuration allows Docker to create 256 networks from172.17.0.0/16.
Docker will allocate subnets172.17.0.0/24,172.17.1.0/24, and so on, up to172.17.255.0/24:
`172.17.0.0/16`
`172.17.0.0/24`
`172.17.1.0/24`
`172.17.255.0/24`
`{"default-address-pools":[{"base":"172.17.0.0/16","size":24}]}`
`{"default-address-pools":[{"base":"172.17.0.0/16","size":24}]}`
You can also request a subnet with a specific prefix length from the default pools by using unspecified
addresses in the--subnetoption:
`$docker network create --ipv6 --subnet ::/56 --subnet 0.0.0.0/24 mynet6686a6746b17228f5052528113ddad0e6d68e2e3905d648e336b33409f2d3b64$docker network inspect mynet -f'{{json .IPAM.Config}}'|jq .[{"Subnet": "172.19.0.0/24","Gateway": "172.19.0.1"},{"Subnet": "fdd3:6f80:972c::/56","Gateway": "fdd3:6f80:972c::1"}]`
`$docker network create --ipv6 --subnet ::/56 --subnet 0.0.0.0/24 mynet6686a6746b17228f5052528113ddad0e6d68e2e3905d648e336b33409f2d3b64$docker network inspect mynet -f'{{json .IPAM.Config}}'|jq .[{"Subnet": "172.19.0.0/24","Gateway": "172.19.0.1"},{"Subnet": "fdd3:6f80:972c::/56","Gateway": "fdd3:6f80:972c::1"}]`
Support for unspecified addresses in--subnetwas introduced in Docker 29.0.0.
If Docker is downgraded to an older version, networks created in this way will become unusable.
They can be removed and re-created, or will function again if the daemon is restored to 29.0.0 or later.

## DNS services

Containers use the same DNS servers as the host by default, but you can
override this with--dns.
By default, containers inherit the DNS settings as defined in the/etc/resolv.confconfiguration file.
Containers that attach to the defaultbridgenetwork receive a copy of this file.
Containers that attach to acustom networkuse Docker's embedded DNS server.
The embedded DNS server forwards external DNS lookups to the DNS servers configured on the host.
The embedded DNS server address is127.0.0.11.
There is no IPv6 equivalent; the IPv4 address works even in IPv6-only containers.
If an application requires an explicit DNS server address, use127.0.0.11.
`/etc/resolv.conf`
You can configure DNS resolution on a per-container basis, using flags for thedocker runordocker createcommand used to start the container.
The following table describes the availabledocker runflags related to DNS
configuration.
`docker create`
`--dns=127.0.0.1`
`--dns-search`
`--dns-search`
`resolv.conf`

## Custom hosts

Your container will have lines in/etc/hostswhich define the hostname of the
container itself, as well aslocalhostand a few other common things. Custom
hosts, defined in/etc/hostson the host machine, aren't inherited by
containers. To pass additional hosts into a container, refer toadd entries to
container hosts filein thedocker runreference documentation.

## Container networks

In addition to user-defined networks, you can attach a container to another
container's networking stack directly, using the--network container:<name|id>flag format.
`--network container:<name|id>`
The following flags aren't supported for containers using thecontainer:networking mode:
--dns-search
`--dns-search`
--dns-option
`--dns-option`
--mac-address
`--mac-address`
--publish-all
`--publish-all`
The following example runs a Redis container, with Redis binding to
127.0.0.1, then running theredis-clicommand and connecting to the Redis
server over 127.0.0.1.
`$docker run -d --name redis redis --bind 127.0.0.1$docker run --rm -it --network container:redis redis redis-cli -h 127.0.0.1`
`$docker run -d --name redis redis --bind 127.0.0.1$docker run --rm -it --network container:redis redis redis-cli -h 127.0.0.1`