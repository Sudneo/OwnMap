from .Errors import UnknownProtocolError, PortOutOfRangeError


class PortState:
    """
    Helper class to classify port possible states.
    1 -> port is open
    2 -> port is closed
    3 -> port state unknown
    """
    PORT_STATE_OPEN = 1
    PORT_STATE_CLOSED = 2
    PORT_STATE_UNK = 3

    def __init__(self):
        pass


class PortProtocol:
    """
    Helper class to determine the protocol for a port.
    1 -> TCP
    2 -> UDP
    3 -> Others
    """
    PROT_TCP = 1
    PROT_UDP = 2
    PROT_OTHER = 3

    def __init__(self):
        pass


class Port(object):
    """
    Class that abstracts the concept of port. Each port has a protocol, a number and a state.
    In addition, ports can have an associated process object.
    Attributes:
        - port_number: the number of the port (ex., 22).
        - port_state: the state of the port (Open or Closed).
        - port_protocol: the port protocol (TCP or UDP).
        - process_running: an optional process running on that port.
        - service: the service running on that port (e.g., SSH)
        - product: the product that runs the service (e.g., OpenSSH)
        - approved: boolean, True if the port is approved, False otherwise
    """
    port_protocol = PortProtocol.PROT_OTHER

    def __init__(self, number, protocol_string):
        if 0 < number <= 65536:
            self.__port_number = number
        else:
            raise PortOutOfRangeError("Ports can only be 1-65536. Value chosen: %s" % number)
        if protocol_string.lower() == "tcp":
            self.port_protocol = PortProtocol.PROT_TCP
        elif protocol_string.lower() == "udp":
            self.port_protocol = PortProtocol.PROT_UDP
        else:
            raise UnknownProtocolError("Port protocol must be TCP or UDP. Cannot be: %s." % protocol_string)
        self.approved = False
        self.comment = ""
        self.service = ""
        self.product = ""
        self.process = ""
        self.port_state = PortState.PORT_STATE_CLOSED

    def open(self):
        self.port_state = PortState.PORT_STATE_OPEN

    def close(self):
        self.port_state = PortState.PORT_STATE_CLOSED

    def unknown_state(self):
        self.port_state = PortState.PORT_STATE_UNK

    @property
    def port_number(self):
        return self.__port_number

    def is_open(self):
        return self.port_state == PortState.PORT_STATE_OPEN

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value

    def is_approved(self):
        return self.approved

    def approve(self):
        self.approved = True

    def disapprove(self):
        self.approved = False

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        self.__product = value

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, value):
        self.__service = value

    @property
    def process(self):
        return self.__process

    @process.setter
    def process(self, value):
        self.__process = value
