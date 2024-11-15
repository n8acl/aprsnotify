import psycopg2 # Postgresql
import pymssql # SQL Server
import pymysql # MySQL
import sqlite3 # SQlite
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import text as sqltext
import json
import os
from os import system

def db_connection(): 
    #############################
    # import config json file For Database connection variables

    config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config.json'))

    with open(config_file, "r") as read_file:
        cfg = json.load(read_file)

    # define SQL connection variables

    sql_host = cfg['database']['credentials']['host']
    sql_user = cfg['database']['credentials']['username']
    sql_password = cfg['database']['credentials']['password']
    sql_database = 'APRSNotify'

    ## Create Engine Object

    if cfg['database']['rdbms_type'] == 'mssql': # SQL Server
        db_uri = 'mssql+pymssql://{0}:{1}@{2}/{3}'.format(sql_user, sql_password, sql_host, sql_database)

    elif cfg['database']['rdbms_type'] == 'mysql': # MySQL/MariaDB
        db_uri = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(sql_user, sql_password, sql_host, sql_database)

    elif cfg['database']['rdbms_type'] == 'postgresql': # PostgreSQL
        db_uri = 'postgresql+psycopg2://{0}:{1}@{2}/{3}'.format(sql_user, sql_password, sql_host, sql_database)

    elif cfg['database']['rdbms_type'] =='sqlite': # SQLite    
        db_uri = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'aprsnotify.db'))        
    
    return sqlalchemy.create_engine(db_uri)