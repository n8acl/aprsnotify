
import pymssql
import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import text as sqltext, select, MetaData, Table
import json
import os
from os import system


import src.db_functions as dbf
import src.db_conn as dbc
import src.db_create as cdb

#############################
# import config json file For Database connection variables

config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'config.json'))

with open(config_file, "r") as read_file:
    cfg = json.load(read_file)

###############################
# Backup old database to new file name if migrating from SQLite to SQLite

if cfg['database']['rdbms_type'] == 'sqlite':
    old_db = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'aprsnotify.db'))
    new_db = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'aprsnotify1.db'))
    os.rename(old_db, new_db)

###############################
# create new database
cdb.create_db()

print("New Database Creation Complete.")
print("Begining Database Migration....")

# Connect New Database
try:
    new_engine = dbc.db_connection()
    print("Database Connection established")
except Exception as e:
    print("Database Connection could not be established.", e)

metadata_new = sqlalchemy.MetaData()
metadata_new.reflect(bind=new_engine)

config_new = metadata_new.tables['config']
apis_new = metadata_new.tables['apis']
callsignlist_new = metadata_new.tables['callsignlist']
services_new = metadata_new.tables['services']

# Connect Old Database
try:
    old_engine = sqlalchemy.create_engine('sqlite:///aprsnotify.db')
    print("Database Connection established")
except Exception as e:
    print("Database Connection could not be established.", e)

metadata_old = sqlalchemy.MetaData()
metadata_old.reflect(bind=old_engine)

config_old = metadata_old.tables['config']
aprsstamps_old = metadata_old.tables['aprsstamps']
callsignlist_old = metadata_old.tables['callsignlists']
apikeys_old = metadata_old.tables['apikeys']

# Migrate Data to new tables

print("Migrating tables...")

# Grab API Keys from old database

sql = sqlalchemy.select(
    apikeys_old.c.telegram_bot_token,
    apikeys_old.c.telegram_club_bot_token,
    apikeys_old.c.telegram_aprsmsg_chat_id,
    apikeys_old.c.telegram_club_chat_id,
    apikeys_old.c.telegram_poswx_chat_id,
    apikeys_old.c.mastodon_client_id,
    apikeys_old.c.mastodon_client_secret,
    apikeys_old.c.mastodon_api_base_url,
    apikeys_old.c.mastodon_user_access_token,
    apikeys_old.c.discord_poswx_wh_url,
    apikeys_old.c.discord_aprsmsg_wh_url,
    apikeys_old.c.discord_club_wh_url,
    apikeys_old.c.mattermost_poswx_wh_url,
    apikeys_old.c.mattermost_poswx_api_key,
    apikeys_old.c.mattermost_aprsmsg_wh_url,
    apikeys_old.c.mattermost_aprsmsg_api_key,
    apikeys_old.c.mattermost_club_wh_url,
    apikeys_old.c.mattermost_club_api_key,
    apikeys_old.c.pushover_token,
    apikeys_old.c.pushover_userkey,
    apikeys_old.c.slack_aprsmsg_wh_url,
    apikeys_old.c.slack_poswx_wh_url,
    apikeys_old.c.slack_club_wh_url,
    apikeys_old.c.aprsfikey
)

apikeys_old_result = dbf.select_sql(old_engine,sql)

for row in apikeys_old_result:
    telegram_bot_token = row[0]
    telegram_club_bot_token = row[1]
    telegram_aprsmsg_chat_id = row[2]
    telegram_club_chat_id = row[3]
    telegram_poswx_chat_id = row[4]
    mastodon_client_id = row[5]
    mastodon_client_secret = row[6]
    mastodon_api_base_url = row[7]
    mastodon_user_access_token = row[8]
    discord_poswx_wh_url = row[9]
    discord_aprsmsg_wh_url = row[10]
    discord_club_wh_url = row[11]
    mattermost_poswx_wh_url = row[12]
    mattermost_poswx_api_key = row[13]
    mattermost_aprsmsg_wh_url = row[14]
    mattermost_aprsmsg_api_key = row[15]
    mattermost_club_wh_url = row[16]
    mattermost_club_api_key = row[17]
    pushover_token = row[18]
    pushover_userkey = row[19]
    slack_aprsmsg_wh_url = row[20]
    slack_poswx_wh_url = row[21]
    slack_club_wh_url = row[22]
    aprsfikey = row[23]

# print(discord_aprsmsg_wh_url)

# Grab Config from old database

sql = sqlalchemy.select(
    config_old.c.telegram,
    config_old.c.slack,
    config_old.c.discord,
    config_old.c.mastodon,
    config_old.c.mattermost,
    config_old.c.units_to_use,
    config_old.c.include_map_image_telegram,
    config_old.c.send_position_data,
    config_old.c.send_weather_data,
    config_old.c.aprsmsg_notify_discord,
    config_old.c.aprsmsg_notify_telegram,
    config_old.c.aprsmsg_notify_pushover,
    config_old.c.aprsmsg_notify_slack,
    config_old.c.aprsmsg_notify_mattermost,
    config_old.c.club_telegram,
    config_old.c.club_discord,
    config_old.c.club_mattermost,
    config_old.c.club_slack
)

config_old_result = dbf.select_sql(old_engine,sql)

for row in config_old_result:
    telegram_flag = row[0]
    slack_flag = row[1]
    discord_flag = row[2]
    mastodon_flag = row[3]
    mattermost_flag = row[4]
    units_to_use = row[5]
    include_map_image_telegram = row[6]
    send_position_data = row[7]
    send_weather_data = row[8]
    aprsmsg_notify_discord = row[9]
    aprsmsg_notify_telegram = row[10]
    aprsmsg_notify_pushover = row[11]
    aprsmsg_notify_slack = row[12]
    aprsmsg_notify_mattermost = row[13]
    club_telegram = row[14]
    club_discord = row[15]
    club_mattermost = row[16]
    club_slack = row[17]


# Grab callsign list from old database

sql = sqlalchemy.select(
    callsignlist_old.c.callsign,
    callsignlist_old.c.listtype,
)

callsignlist_old_result = dbf.select_sql(old_engine,sql)

# Grab Stamps data from Old Database

sql = sqlalchemy.select(
    aprsstamps_old.c.lastpostime,
    aprsstamps_old.c.lastmsgid,
    aprsstamps_old.c.lastwxtime
)

aprsstamps_old_result = dbf.select_sql(old_engine,sql)

for row in aprsstamps_old_result:
    lastpostime = row[0]
    lastmsgid = row[1]
    lastwxtime = row[2]

##### Migrate data to new tables

# Insert callsign list data

for row in callsignlist_old_result:
    sql = callsignlist_new.insert()
    values_list =[{'callsign':row[0],'listtype': row[1]}]

    dbf.insert_sql(new_engine,sql,values_list)

# insert Old apikeys data
# sql = apikeys_new.insert()
# values_list = [{'apiname':"aprsfi", 
#                 'apikey': aprsfikey }]
# dbf.insert_sql(new_engine,sql,values_list)


######### Start inserting service data

## Insert Telegram data
if telegram_flag:
    sql = services_new.insert()
    values_list = [{'service_name':"Telegram", 
                    'friendlyname': "Personal",
                    'active': True,
                    'service_url': 'tgram://' + telegram_bot_token + '/' + telegram_poswx_chat_id + '/',
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)

if club_telegram:
    sql = services_new.insert()
    values_list = [{'service_name':"Telegram", 
                    'friendlyname': "Club",
                    'active': True,
                    'service_url': 'tgram://' + telegram_club_bot_token + '/' + telegram_club_chat_id + '/',
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)

if aprsmsg_notify_telegram:
    if telegram_aprsmsg_chat_id == '' and telegram_flag:
        sql = services_new.update().where((services_new.c.service_name == 'Telegram') & (services_new.c.friendlyname == 'Personal')).values(send_msg_data=aprsmsg_notify_telegram)

        dbf.exec_sql(new_engine,sql)
    else:

        sql = services_new.insert()
        values_list = [{'service_name':"Telegram", 
                        'friendlyname': "Messaging",
                        'active': True,
                        'service_url': 'tgram://' + telegram_bot_token + '/' + telegram_aprsmsg_chat_id + '/',
                        'send_pos_data': False,
                        'send_msg_data': aprsmsg_notify_telegram,
                        'send_wx_data': False
            }]

        dbf.insert_sql(new_engine,sql,values_list)

## Insert Mastodon data //TODO This code block will need to be removed so that apprise support can be setup correctly.
# if mastodon_flag:
#     sql = mastodon_new.insert()
#     values_list = [{'name': 'Personal',
#                     'client_id': mastodon_client_id,
#                     'client_secret': mastodon_client_secret,
#                     'api_base_url': mastodon_api_base_url,
#                     'user_access_token': mastodon_user_access_token,
#                     'send_pos_data': send_position_data,
#                     'send_msg_data': False,
#                     'send_wx_data': send_weather_data

#     }]

#     dbf.insert_sql(new_engine,sql,values_list)

## Insert Discord data

if discord_flag:
    sql = services_new.insert()
    values_list = [{'service_name':"Discord", 
                    'friendlyname': "Personal",
                    'active': True,
                    'service_url': discord_poswx_wh_url,
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)

if aprsmsg_notify_discord:
    if discord_aprsmsg_wh_url == '' and discord_flag:
        sql = services_new.update().where((services_new.c.service_name == 'Discord') & (services_new.c.friendlyname == 'Personal')).values(send_msg_data=aprsmsg_notify_discord)

        dbf.exec_sql(new_engine,sql)
    else:
        sql = services_new.insert()
        values_list = [{'service_name':"Discord", 
                        'friendlyname': "Messaging",
                        'active': True,
                        'service_url': discord_aprsmsg_wh_url,
                        'send_pos_data': False,
                        'send_msg_data': aprsmsg_notify_discord,
                        'send_wx_data': False
            }]

        dbf.insert_sql(new_engine,sql,values_list)

if club_discord:
    sql = services_new.insert()
    values_list = [{'service_name':"Discord", 
                    'friendlyname': "Club",
                    'active': True,
                    'service_url': discord_club_wh_url,
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)

## Insert Mattermost data //TODO This will need to be removed to handle new apprise changes
# if mattermost_flag:
#     sql = mattermost_new.insert()
#     values_list = [{'name': 'Personal',
#                     'apikey': mattermost_poswx_api_key,
#                     'webhook_url': mattermost_poswx_wh_url,
#                     'send_pos_data': send_position_data,
#                     'send_wx_data': send_weather_data

#     }]

#     dbf.insert_sql(new_engine,sql,values_list)

# if aprsmsg_notify_mattermost:
#     if mattermost_aprsmsg_wh_url == '' and mattermost_flag:
#         sql = mattermost_new.update().where(mattermost_new.c.name == 'Personal').values(send_msg_data=aprsmsg_notify_mattermost)

#         dbf.exec_sql(new_engine,sql)
#     else:
#         sql = mattermost_new.insert()
#         values_list = [{'name': 'Messaging',
#                         'apikey': mattermost_aprsmsg_api_key,
#                         'webhook_url': mattermost_aprsmsg_wh_url,
#                         'send_msg_data': aprsmsg_notify_mattermost

#         }]

#         dbf.insert_sql(new_engine,sql,values_list)

# if club_mattermost:
#     sql = mattermost_new.insert()
#     values_list = [{'name': 'Club',
#                     'apikey': mattermost_club_api_key,
#                     'webhook_url': mattermost_club_wh_url,
#                     'send_pos_data': send_position_data,
#                     'send_wx_data': send_weather_data

#     }]

#     dbf.insert_sql(new_engine,sql,values_list)

## Insert Pushover Data

if aprsmsg_notify_pushover:
    sql = services_new.insert()
    values_list = [{'service_name':"Pushover", 
                    'friendlyname': "Messaging",
                    'active': True,
                    'service_url': 'pover://' + pushover_userkey + '@' + pushover_token,
                    'send_pos_data': False,
                    'send_msg_data': aprsmsg_notify_pushover,
                    'send_wx_data': False
        }]

    dbf.insert_sql(new_engine,sql,values_list)

## Insert Slack Data

if slack_flag:
    sql = services_new.insert()
    values_list = [{'service_name':"Slack", 
                    'friendlyname': "Personal",
                    'active': True,
                    'service_url': slack_poswx_wh_url,
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)

if aprsmsg_notify_slack:
    if slack_aprsmsg_wh_url == '' and slack_flag:
        sql = services_new.update().where((services_new.c.service_name == 'Slack') & (services_new.c.friendlyname == 'Personal')).values(send_msg_data=aprsmsg_notify_slack)

        dbf.exec_sql(new_engine,sql)
    else:
        sql = services_new.insert()
        values_list = [{'service_name':"Slack", 
                        'friendlyname': "Messaging",
                        'active': True,
                        'service_url': slack_poswx_wh_url,
                        'send_pos_data': False,
                        'send_msg_data': aprsmsg_notify_slack,
                        'send_wx_data': False
            }]

        dbf.insert_sql(new_engine,sql,values_list)

if club_slack:
    sql = services_new.insert()
    values_list = [{'service_name':"Slack", 
                    'friendlyname': "Club",
                    'active': True,
                    'service_url': slack_club_wh_url,
                    'send_pos_data': send_position_data,
                    'send_msg_data': False,
                    'send_wx_data': send_weather_data
        }]

    dbf.insert_sql(new_engine,sql,values_list)


## Update table Values

# Update Config
sql = config_new.update().where((config_new.c.setting_name == 'units_to_use')).values(setting_value_int=units_to_use)

dbf.exec_sql(new_engine,sql)

# Update aprsfi key in Apis

sql = apis_new.update().where((apis_new.c.apiname == 'aprsfi')).values(apikey=aprsfikey)

dbf.exec_sql(new_engine,sql)


# Update Last time stamps
sql = callsignlist_new.update().where(callsignlist_new.c.listtype == 'POS').values(last_timestamp=lastpostime)

dbf.exec_sql(new_engine,sql)

sql = callsignlist_new.update().where(callsignlist_new.c.listtype == 'MSG').values(last_timestamp=lastmsgid)

dbf.exec_sql(new_engine,sql)

sql = callsignlist_new.update().where(callsignlist_new.c.listtype == 'WX').values(last_timestamp=lastwxtime)

dbf.exec_sql(new_engine,sql)