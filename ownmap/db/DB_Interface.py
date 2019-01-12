from ownmap.config.Config import ConfigReader
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
    ip = host_object.ip_address
    params = config()
    ports = []
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
        result = cur.fetchall()
    except psycopg2.DatabaseError as Error:
        logging.error(Error)
    finally:
        if conn is not None:
            conn.close()


def __load_hosts():
    pass


def load_state():
    pass


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
