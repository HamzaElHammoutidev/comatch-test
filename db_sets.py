import psycopg2
import pandas as pd
import logging
from configparser import ConfigParser
import psycopg2.extras


logging.basicConfig(level = logging.INFO)

def load_settings():
    """
    Loads settings from files

    :return: dictionary with settings key-value pairs.
    """

    config = ConfigParser()
    config.read("settings.ini")

    return {
        "host":config.get("postgres","host"),
        "database":config.get("postgres","database"),
        "user":config.get("postgres","user"),
        "password":config.get("postgres","password")
    }

def connect():
    """
    Connects User to Database

    :return: postgres connection.
    """
    conn = None
    settings = load_settings()
    params = {
        "host" : settings["host"],
        "database": settings["database"],
        "user":settings["user"],
        "password":settings["password"]
    }
    try:
        conn = psycopg2.connect(**params)
        logging.info("Connection successfully set!")
        return conn
    except (Exception,psycopg2.DatabaseError) as e:
        logging.error(e)

def create_database(conn,database_name):
    """
    Creates database in PostgresSQL SERVER

    :param conn: PostgresSQL server connection.
    :param database_name: SQL table creation query.
    :return: None.
    """
    conn.autocommit = True

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = {}".format(database_name))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE {}".format(database_name))
    except Exception as e:
        logging.error(e)

def create_table(conn,creation_script):
    """
    Creates table in PostgresSQL SERVER

    :param conn: PostgresSQL server connection.
    :param table_name: SQL table.
    :param creation_table: SQL table creation query.
    :return: None.
    """


    try:
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(creation_script)
        cursor.close()
    except psycopg2.OperationalError as e:
        logging.error(e)

def transact_query(conn,query):
    """
    DELETE/UPDATE/INSERT data into PostgresSQL Table

    :param conn: PostgresSQL server connection.
    :param query: SQL query.
    """

    try:
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(query)
        cursor.close()
    except psycopg2.OperationalError as e:
        logging.error(e)


def execute_values(conn,df,table):
    """
    Using psycopg2.extra.execute_values to bulk insert data from Dataframe into Table.

    :param conn: PostgresSQL server connection.
    :param df: Pandas Dataframe.
    :param table: SQL Table name.
    :return: None.
    """

    try:
        # Convert Df values into tupples
        tuples = [tuple(x) for x in df.to_numpy()]
        # Seperate different columns by comma.
        #print(df.columns)

        columns = ','.join(list(df.columns))
        # Sql Query to bulk insert
        query = "INSERT INTO %s(%s) VALUES %%s" % (table,columns)
        cursor = conn.cursor()
        psycopg2.extras.execute_values(cursor,query,tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        logging.error(e)
        conn.rollback()
        cursor.close()
        return 1
    logging.info("execute values() done")
    cursor.close()


def analytics_query(conn,query):
    """
    Executes and gets back analytics queries from PostgresSQL DB

    :param conn: PostgresSQL server connection.
    :param query: SQL query.
    """

    try:
        data = None
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(query)
        data =  cursor.fetchall()
        cursor.close()
    except psycopg2.OperationalError as e:
        logging.error(e)
    return data[0][0]