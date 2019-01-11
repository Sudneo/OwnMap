from ownmap.config.Config import ConfigReader
import psycopg2
import logging


def get_targets():
    configreader = ConfigReader(filename="config.yaml")
    params = configreader.get_config_section("postgresql")
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
