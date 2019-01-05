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


class Port:
    """
    Class that abstracts the concept of port. Each port has a protocol, a number and a state.
    In addition, ports can have an associated process object.
    Attributes:
        - port_number: the number of the port (ex., 22).
        - port_state: the state of the port (Open or Closed).
        - port_protocol: the port protocol (TCP or UDP).
        - process_running: an optional process running on that port.
    """
    port_state = PortState.PORT_STATE_CLOSED
    port_protocol = PortProtocol.PROT_OTHER
    process_running = None

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
