from ownmap import Host as Host
from ownmap.Errors import *
from ownmap import Port as Port
from ownmap import State as State
import json
import pprint


def main():
    host_a = Host.Host(ip='127.0.0.1')
    host_a.host_name = "a"
    port_a_22 = Port.Port(22, 'tcp')
    port_a_21 = Port.Port(21, 'tcp')
    host_a.add_port(port_a_21)
    host_a.add_port(port_a_22)
    host_a.ssh_available = True
    new_host = Host.Host(ip='192.168.1.131')
    host_b = Host.Host(dns='localhost')
    host_b.host_name = "b"
    port_22 = Port.Port(22, 'tcp')
    port_22.service = 'ssh'
    port_22.approve()
    host_b.add_port(port_22)
    host_b.add_port(Port.Port(21, 'tcp'))

    state_a = State.State()
    state_a.add_hosts(host_a)
    state_a.add_hosts(new_host)
    state_b = State.State()
    state_b.add_hosts(host_b)

    delta = State.State.compare(state_a, state_b)
    pprint.pprint(delta['127.0.0.1'].get_differences())

main()