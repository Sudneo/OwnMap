class Error(Exception):
    pass


class PortMisuseError(Error):
    """
    Exception raised when trying to change the port number of a port object.
    """

    def __init__(self, message):
        self.message = message


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


class ProcessMisuseError(Error):
    """
    Exception raised when trying to change the process string to a process object.
    """
    def __init__(self, message):
        self.message = message