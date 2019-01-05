import socket
import ipaddress
import logging
from .Port import Port


class Host:
    """
    Class that abstracts the concept of host. Each host has several characteristics from OwnMap perspective.
    Each host has a unique IP address, an optional hostname, an optional dns name, optional SSH parameters to connect,
    and a list of ports.
    Attributes:
         - host_alive: boolean, True if the host is alive, False otherwise
         - ip_addr: the IP address used to scan the host.
         - host_name: the hostname of the machine (e.g., /etc/hostname)
         - dns_name: a DNS name that resolves to the IP of the host. Note that if an host is created with both an IP
         and a DNS name, the DNS name will be resolved and the IP will be overwritten.
         - ssh_available: boolean, True if it is possible to SSH into the host, False otherwise.
         - ssh_username: the username to use for connecting via SSH (defaults to the user executing the tool).
         - ports[]: a list of (open) ports associated with the host.
    """
    host_name = ""
    dns_name = ""
    ports = []

    def __init__(self, ip="", dns="", host_alive=False, ssh_available=False, ssh_username=""):
        assert ip != "" or dns != ""
        if ip != "" and dns != "":
            # If both IP and DNS name are passed
            try:
                # Try to resolve the DNS name
                ip_resolved = ipaddress.ip_address(socket.gethostbyname(dns))
                if ip_resolved != ipaddress.ip_address(ip):
                    # If the IP resolved is different from the one passed, warn the user and override it
                    logging.warning("DNS name  %s passed as parameter resolves with a different IP (%s) "
                                    "from the one passed (%s).", dns, str(ip_resolved), str(ip))
                self.__ip_address = ip_resolved
                self.dns_name = dns
            except socket.gaierror:
                # If DNS name resolution fails
                logging.error("DNS name %s could not be resolved, falling back to IP %s.", dns, ip)
                try:
                    # Validate IP
                    ip_validated = ipaddress.ip_address(ip)
                    # If IP is valid, use the IP
                    self.__ip_address = ip_validated
                    # Resolve the IP and override DNS
                    self.dns_name = socket.gethostbyaddr(str(ip_validated))[0]
                except ValueError:
                    # If the IP is invalid, then we cannot create a host (IP and DNS invalid)
                    logging.error("IP address %s is not a valid IP.", ip)
                    raise ValueError("IP address %s is not a valid IP" % ip)
        elif ip != "":
            # dns_name == "" and ip_addr not ""
            try:
                ip_validated = ipaddress.ip_address(ip)
                self.__ip_address = ip_validated
                self.dns_name = socket.gethostbyaddr(str(ip_validated))[0]
            except ValueError:
                logging.error("IP address %s is not a valid IP.", ip)
                raise ValueError("IP address %s is not a valid IP" % ip)
        else:
            # dns_name not "" and ip_addr ""
            self.dns_name = dns
            try:
                self.__ip_address = ipaddress.ip_address(socket.gethostbyname(self.dns_name))
            except socket.gaierror:
                logging.error("DNS name %s could not be resolved, IP not provided, failing to create host.", dns)
                raise ValueError("DNS not valid for host where IP is not provided.")
        # IP address at this point has been set
        self.host_alive = host_alive
        self.ssh_available = ssh_available
        self.ssh_username = ssh_username

    @property
    def ip_address(self):
        return str(self.__ip_address)

    @property
    def host_alive(self):
        return self.__host_alive

    @host_alive.setter
    def host_alive(self, host_alive):
        assert isinstance(host_alive, bool)
        if host_alive:
            self.__host_alive = True
        else:
            self.__host_alive = False

    @property
    def ssh_available(self):
        return self.__ssh_available

    @ssh_available.setter
    def ssh_available(self, value):
        assert isinstance(value, bool)
        if value:
            self.__ssh_available = True
        else:
            self.__ssh_available = False

    @property
    def ssh_username(self):
        return self.__ssh_username

    @ssh_username.setter
    def ssh_username(self, value):
        self.__ssh_username = value

    def add_port(self, port):
        assert isinstance(port, Port)
        self.ports.append(port)

    def get_ports(self):
        return self.ports

    def get_open_ports(self):
        open_ports = []
        for port in self.ports:
            if port.is_open():
                open_ports.append(port)
        return open_ports
