from ownmap.config.Config import ConfigReader
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
# docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=password -d postgres


def config():
    """
    Returns postgresql specific parameters from config file.
    """
    configreader = ConfigReader(filename="config.yaml")
    params = configreader.get_config_section("postgresql")
    return params


def create_database():
    """
    Create necessay DB in postgres, use default postgres db to create it.
    """
    logging.debug("Starting process to create database.")
    db_name = config()['database']
    command = "CREATE DATABASE %s" % db_name
    logging.debug("Command prepared: %s." % command)
    conn = None
    try:
        # read the connection parameters
        params = config()
        params['database'] = "postgres"
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
        logging.info("Database %s created." % db_name)


def create_tables():
    """
    create tables in the PostgreSQL database
    """
    logging.debug("Starting process to create database tables.")
    commands = (
        """
        CREATE TABLE hosts (
            host_ip INET PRIMARY KEY,
            alive BOOLEAN,
            dns_name VARCHAR(255),
            host_name VARCHAR(255),
            ssh_available BOOLEAN,
            ssh_user VARCHAR(255),
            added DATE NOT NULL DEFAULT CURRENT_DATE,
            last_modified DATE
        )
        """,
        """ CREATE TABLE ports (
                host_ip INET,
                port INT,
                process VARCHAR(1000),
                service VARCHAR(1000),
                product VARCHAR(1000),
                protocol VARCHAR(20),
                state VARCHAR(20),
                added DATE NOT NULL DEFAULT CURRENT_DATE,
                last_modified DATE,
                approved BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (host_ip, port)
                )
        """,
        """ CREATE TABLE targets (
                ip INET PRIMARY KEY 
            )        
        """)
    for command in commands:
        logging.debug("Command prepared: %s" % command)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        logging.info("Tables created.")


def prepare_database():
    """
    Create database and tables.
    """
    create_database()
    create_tables()
