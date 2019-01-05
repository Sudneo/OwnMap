from ownmap import Host as Host
from ownmap.Errors import *
from ownmap import Port as Port


def main():
    host = Host.Host(ip='127.0.0.1')
    # host.ip_address = "bla"
    host = Host.Host(ip='127.0.0.1', dns='localhost')
    # host.ip_address = '1.1.1.1'
    # host.__ip_address = '1.1.1.1'
    host = Host.Host(ip='1.1.1.1', dns='localhost')
    p = Port.Port(54, "tcp")
    print(p.port_number)
    host.add_port(p)


if __name__ == '__main__':
    main()