import sqlalchemy as db
# from sqlalchemy import text as sqltext, select, MetaData, Table, Column
from sqlalchemy_utils import database_exists, create_database

import src.db_functions as dbf
import src.db_conn as dbc

def create_db():

    #############################
    # Define Database Engine

    try:
        db_engine = dbc.db_connection()
        print("Database Connection established")
    except Exception as e:
        print("Database Connection could not be established.", e)

    #############################
    # create new Database

    print("Creating Database....")

    create_database(db_engine.url)

    metadata = db.MetaData()

    print("Creating Tables....")

    callsignlist = db.Table('callsignlist', metadata,
                    db.Column('callsign',db.String(10)),
                    db.Column('listtype',db.String(5)),
                    db.Column('last_timestamp',db.Integer())
    )

    services = db.Table('services', metadata,
                    db.Column('service_name',db.String(50)),
                    db.Column('friendlyname',db.String(1000)),
                    db.Column('active',db.Boolean()),
                    db.Column('service_url',db.String(1000)),
                    db.Column('send_pos_data',db.Boolean()),
                    db.Column('send_msg_data',db.Boolean()),
                    db.Column('send_wx_data',db.Boolean()),

    ) 

    apis = db.Table('apis', metadata,
                    db.Column('apiname',db.String(50)),
                    db.Column('apikey',db.String(100)),
                    db.Column('apiurl',db.String(1000))
    ) 

    config = db.Table('config', metadata,
                    db.Column('setting_name',db.String(500)),
                    db.Column('setting_value_int',db.Integer()),
                    db.Column('setting_value_boolean',db.Boolean()),
                    db.Column('setting_value_text',db.String(1000))
    )

    supportedservices = db.Table('supportedservices', metadata,
                    db.Column('service_name',db.String(50)),
    
    ) 

    metadata.create_all(db_engine)


    #############################
    # Insert Default Data into Database

    metadata.reflect(bind=db_engine)

    # services = metadata.tables['services']
    config = metadata.tables['config']
    apis = metadata.tables['apis']

    print("Inserting Default Data....")

    # insert apiurls data

    sql = apis.insert()
    values_list = [{'apiname':'aprsfi', 'apikey': '', 'apiurl': "https://api.aprs.fi/api/get"},
                    {'apiname':'wx_api','apikey': '', 'apiurl': "http://api.weatherapi.com/v1/forecast.json"},
                    {'apiname':'apprise_api','apikey': 'aprsnotify', 'apiurl': "http://localhost:8000/notify/"}
    ]

    dbf.insert_sql(db_engine,sql,values_list)


    # insert config data
    sql = config.insert()
    values_list = [{'setting_name':'units_to_use', 'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': ''}, # Default to Imperial Units
                    {'setting_name':'delay_time',  'setting_value_int': 600, 'setting_value_boolean':False, 'setting_value_text': ''}, # Default to 10 Minutes
                    {'setting_name':'use_apprise_api',  'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': ''}, # Default to native installation
                    {'setting_name':'apprise_api_pos_tags',  'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': 'POS'}, # Default POS Tag
                    {'setting_name':'apprise_api_wx_tags',  'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': 'WX'}, # Default WX Tag
                    {'setting_name':'apprise_api_msg_tags',  'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': 'MSG'}, # Default MSG Tag
                    {'setting_name':'user_timezone',  'setting_value_int': 0, 'setting_value_boolean':False, 'setting_value_text': 'America/New_York'}, # Default TimeZone
    ]

    dbf.insert_sql(db_engine,sql,values_list)

    # insert Supported Services data

    sql = supportedservices.insert()
    values_list = [{'service_name':'DAPNET'},
                    {'service_name':'Discord'},
                    {'service_name':'Mastodon'},
                    {'service_name':'Matrix'},
                    {'service_name':'Mattermost'},
                    {'service_name':'Pushover'},
                    {'service_name':'Signal'},
                    {'service_name':'Slack'},
                    {'service_name':'Telegram'},
    ]

    dbf.insert_sql(db_engine,sql,values_list)