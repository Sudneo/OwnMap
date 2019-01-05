class Process:
    """
    Class used to abstract the concept of a process running on a specific port.
    Attributes:
        - process_string
    """
    def __init__(self, process_string):
        self.__process_string = process_string

    @property
    def process_string(self):
        return self.__process_string
