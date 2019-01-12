from ownmap import Port, Host, State
from ownmap.db.DB_Interface import *
from multiprocessing.dummy import Pool as ThreadPool
import nmap
import logging
import datetime


class Portscan(object):
    """
    Class used to abstract the concept of a portscan.
    A portscan has the following attributes:
        - targets: the list of the targets (hosts) to scan
        - state: an instance of the State class
    """
    def __init__(self):
        self.__targets = get_targets()
        self.__state = State.State()
        self.__state.date = datetime.datetime.now()

    @property
    def targets(self):
        return self.__targets

    @property
    def state(self):
        return self.__state

    def scan_host(self, host):
        """
        Function meant to be multithreaded to portscan one host. It creates one instance of the Host class, adds the
        relevant ports to it and then adds it to self.state
        :param host: The host to scan
        :return: None
        """
        host_object = Host(host)
        nmap_scan = nmap.PortScanner()
        nmap_scan.scan(host, '1-100')
        try:
            # Check if the host was up.
            host_info = nmap_scan[host]
            host_object.host_alive = True
        except KeyError:
            # If the host was down, mark it as non alive, add it to the state and return.
            logging.debug("Host %s is down." % host)
            host_object.host_alive = False
            self.state.add_hosts(host_object)
            return

        # If the host is alive check TCP ports
        try:
            # Check if there are tcp ports discovered
            tcp_ports = host_info['tcp']
            # For each port found
            for port in tcp_ports.keys():
                # Create new port object and fill the information
                port_object = Port(port, 'tcp')
                port_info = tcp_ports[port]
                # If the port is open
                if port_info['state'] == 'open':
                    port_object.open()
                    # Try to get service and product (e.g., HTTP, Nginx v1.10.3)
                    port_object.service = port_info['name']
                    product_version = port_info['version']
                    if len(port_info['product']) > 0:
                        product_string = port_info['product']
                        if len(product_version) > 0:
                            product_string = "%s v%s" % (product_string, product_version)
                        port_object.product = product_string
                else:
                    port.close()
                host_object.add_port(port_object)
        except KeyError:
            logging.info("No tcp ports open on host %s." % host)
        try:
            # Check if there are UDP ports discovered
            tcp_ports = host_info['udp']
            # For each port found
            for port in tcp_ports.keys():
                # Create new port object and fill the information
                port_object = Port(port, 'udp')
                port_info = tcp_ports[port]
                # If the port is open
                if port_info['state'] == 'open':
                    port_object.open()
                    # Try to get service and product (e.g., HTTP, Nginx v1.10.3)
                    port_object.service = port_info['name']
                    product_version = port_info['version']
                    if len(port_info['product']) > 0:
                        product_string = port_info['product']
                        if len(product_version) > 0:
                            product_string = "%s v%s" % (product_string, product_version)
                        port_object.product = product_string
                else:
                    port.close()
                host_object.add_port(port_object)
        except KeyError:
            logging.info("No tcp ports open on host %s." % host)
        finally:
            self.state.add_hosts(host_object)

    def run(self):
        """
        Function that runs the scan in multithreaded mode.
        :return:
        """
        # Main function to run the scan
        thread_pool = ThreadPool(4)
        # Every call for scan host will scan a different host and will add the scanned host to the self.state
        thread_pool.map(self.scan_host, self.targets)

    def save_state(self):
        save_state(self.state)
