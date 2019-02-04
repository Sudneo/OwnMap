from ownmap.config.Config import ConfigReader
from ownmap.State import State
from ownmap.Host import Host
from ownmap.Port import Port, PortProtocol, PortState
import psycopg2
import logging


def config():
    configreader = ConfigReader(filename="config.yaml")
    params = configreader.get_config_section("postgresql")
    return params


def get_targets():
    params = config()
    targets = []
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        select_query = '''
                        select ip 
                        from targets
                        '''
        cur.execute(select_query)
        result = cur.fetchall()
        for item in result:
            targets.append(item[0])
    except psycopg2.DatabaseError as Error:
        logging.error(Error)
    finally:
        if conn is not None:
            conn.close()
    return targets


def __load_ports(host_object):
    """
    Utility function used to load all the ports in the DB for a given host
    :param host_object: The host object to gather the ports of
    :return: A list of Port objects
    """
    ip = host_object.ip_address
    params = config()
    ports_list = []
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        select_query = '''
        select *
        from ports
        where host_ip = %s
        '''
        cur.execute(select_query, (ip,))
        ports = cur.fetchall()
        for port in ports:
            host_ip, port, process, service, product, protocol, state, added, last_modified, approved = port
            # Set the port protocol
            if int(protocol) == PortProtocol.PROT_TCP:
                protocol = "tcp"
            elif int(protocol) == PortProtocol.PROT_UDP:
                protocol = "udp"
            else:
                protocol = "other"
            # Create port object
            port_object = Port(number=port, protocol_string=protocol)
            # Set the port state
            if state == PortState.PORT_STATE_OPEN:
                port_object.open()
            else:
                port_object.close()
            # Set the port approval
            if approved:
                port_object.approve()
            else:
                port_object.disapprove()
            # Set other attributes
            port_object.service = service
            port_object.product = product
            port_object.process = process
            ports_list.append(port_object)
    except psycopg2.DatabaseError as Error:
        logging.error(Error)
    finally:
        if conn is not None:
            conn.close()
    return ports_list


def __load_hosts():
    """
    Utility function to load all the hosts from the DB
    :return: A list of Host objects present in the database
    """
    hosts_list = []
    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        select_query = '''
            select *
            from hosts
            '''
        cur.execute(select_query)
        hosts = cur.fetchall()
        for host in hosts:
            ip, alive, dns, hosts, ssh_available, ssh_username, added, last_modified = host
            host_object = Host(ip=ip, host_alive=alive, dns=dns, ssh_available=ssh_available, ssh_username=ssh_username)
            ports = __load_ports(host_object)
            for p in ports:
                host_object.add_port(p)
            hosts_list.append(host_object)
    except psycopg2.DatabaseError as Error:
        logging.error(Error)
    finally:
        if conn is not None:
            conn.close()
    return hosts_list


def load_state():
    """
    This function is used to load the state from the DB.
    :return: A State object which represents the current state
    """
    state_object = State()
    hosts = __load_hosts()
    for host in hosts:
        state_object.add_hosts(host)
    return state_object


def __save_port(port, ip):
    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        insert_query = '''      
                                INSERT INTO ports (host_ip, port, service, protocol, product, 
                                state, last_modified, approved) 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                                '''
        cur.execute(insert_query, (ip, port.port_number, port.service, port.port_protocol, port.product,
                                   port.port_state, "NOW()", port.is_approved(),))
        conn.commit()
    except psycopg2.DatabaseError as error:
        if conn:
            conn.rollback()
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()


def __save_host(host):
    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        insert_query = '''      
                                   INSERT INTO hosts (host_ip, alive, dns_name, host_name, ssh_available, ssh_user, last_modified) 
                                   VALUES(%s, %s, %s, %s, %s, %s, %s)
                                   '''
        cur.execute(insert_query, (host.ip_address, host.host_alive, host.dns_name, host.host_name, host.ssh_available,
                                   host.ssh_username, "NOW()",))
        conn.commit()
    except psycopg2.DatabaseError as error:
        if conn:
            conn.rollback()
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
    for port in host.ports:
        __save_port(port, host.ip_address)


def save_state(state):
    """
    Functions used to save the current state to the database.
    A state has different hosts each with different ports.
    The function deletes the current host and port tables to effectively overwrite the changes.
    :param state: The state object to save in the DB.
    :return: None
    """
    params = config()
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = '''
                TRUNCATE ports, hosts
                '''
        cur.execute(query)
        conn.commit()
        for host_object in state.hosts:
            __save_host(host_object)
    except psycopg2.DatabaseError as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
