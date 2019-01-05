from Errors import ProcessMisuseError


class Process:
    """
    Class used to abstract the concept of a process running on a specific port.
    Attributes:
        - process_string
    """
    def __init__(self, process_string):
        self.process_string = process_string

    @property
    def process_string(self):
        return self.process_string

    @process_string.setter
    def process_string(self, value):
        raise ProcessMisuseError("Cannot change the process string of a process after this has been initialized.")
