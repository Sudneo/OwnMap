class Error(Exception):
    pass


class UnknownProtocolError(Error):
    """
    Exception raised when trying to create a port with a protocol different from TCP or UDP
    """
    def __init__(self, message):
        self.message = message


class PortOutOfRangeError(Error):
    """
    Exception raised when trying to create a port with number outside [1,65356] range.
    """
    def __init__(self, message):
        self.message = message
