class StateDelta:
    """
    Helper class used to store the difference between two states.
    """
    hosts_added = []
    hosts_removed = []

    def __init__(self):
        self.host_differences = []

    def add_host(self, host):
        self.hosts_added.append(host)

    def remove_host(self, host):
        self.hosts_removed.append(host)

    def get_new_hosts(self):
        return self.hosts_added

    def get_old_hosts(self):
        return self.hosts_removed

    @property
    def host_differences(self):
        return self.host_differences

    @host_differences.setter
    def host_differences(self, value):
        self.host_differences = value


class PortDelta:
    """
    Helper class used to store the difference (e.g., what changed) between two ports with the same number.
    """
    state_changed = False
    process_changed = False
    service_changed = False
    product_changed = False
    approved_changed = False
    comment_changed = False

    def __init__(self, port_a, port_b):
        if port_a.port_state != port_b.port_state:
            self.state_changed = True
        if port_a.process != port_b.process:
            self.process_changed = True
        if port_a.product != port_b.product:
            self.product_changed = True
        if port_a.service != port_b.service:
            self.service_changed = True
        if port_a.is_approved() != port_b.is_approved():
            self.approved_changed = True
        if port_a.comment != port_b.comment:
            self.comment_changed = True

    def get_differences(self):
        delta = {
            'changes':
                {
                    'state': self.state_changed,
                    'process': self.process_changed,
                    'service': self.service_changed,
                    'product': self.product_changed,
                    'comment': self.comment_changed,
                    'approved': self.approved_changed
                }
                }
        changes = self.state_changed or self.process_changed or self.service_changed or \
                  self.product_changed or self.comment_changed or self.approved_changed
        return delta, changes


class HostDelta:
    """
    Helper class used to store the difference (e.g., what changed) between two hosts with the same IP.
    """
    alive_changed = False
    dns_changed = False
    ports_changed = False
    ports_delta = None

    def __init__(self, host_a, host_b):
        if host_a.dns_name != host_b.dns_name:
            self.dns_changed = True
        if host_a.host_alive != host_b.host_alive:
            self.alive_changed = True
        for port_a in host_a.get_ports():
            # for every port in the old state
            for port_b in host_b.get_ports():
                if port_b.port_number == port_a.port_number and port_b.port_protocol == port_a.protocol:
                    # They are the same port, compare state and other fields.
                    delta, changed = PortDelta(port_a, port_b).get_differences()
                    if changed:
                        self.ports_changed = True
                        self.ports_delta.append({port_a.port_number: delta})

    def get_differences(self):
        delta = {
            'host_changes':
                {
                    'alive': self.alive_changed,
                    'dns': self.dns_changed,
                    'ports': self.ports_changed,
                    'port_changes': self.ports_delta
                 }
                 }
        return delta


class State:
    """
    This class abstracts the concept of a state. A state is a condition in which certain hosts have certain ports open
    at a specific time (and date). The state is loaded from the database and saved back to it.
    """

    def __init__(self):
        self.__hosts = []
        self.__date = None

    @property
    def hosts(self):
        return self.__hosts

    def add_hosts(self, host):
        self.__hosts.append(host)

    def load(self):
        # Read from DB and populate hosts var
        pass

    def save(self):
        # Save hosts to database
        pass

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @staticmethod
    def __hosts_delta(hosts_a, hosts_b):
        host_delta = {}
        for host_a in hosts_a:
            for host_b in hosts_b:
                if host_a.ip_address == host_b.ip_address:
                    # They are the same hosts
                    delta = HostDelta(host_a, host_b)
                    host_delta[host_a.ip_address] = delta
        return host_delta

    @staticmethod
    def compare(state_a, state_b):
        """
        Utility function used to compare two states.
        :param state_a: The first state (older)
        :param state_b: The new state (current)
        :return: an object of class StateDelta
        """
        state_delta = StateDelta()
        # Compute hosts which are in b but not in a
        for host_b in state_b.hosts:
            present = False
            for host_a in state_a.hosts:
                if host_b.ip_address == host_a.ip_address:
                    present = True
            if not present:
                state_delta.add_host(host_b)
        # Compute hosts which are in a but not in b
        for host_a in state_a.hosts:
            present = False
            for host_b in state_b.hosts:
                if host_a.ip_address == host_b.ip_address:
                    present = True
            if not present:
                state_delta.remove_host(host_a)
        # Compute port differences between hosts in a which are also in b
        state_delta.host_differences = State.__hosts_delta(state_b.hosts, state_b.hosts)
