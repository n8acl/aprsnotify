# Import libraries
import sqlite3
import os
from os import system, name
from sqlite3 import Error

# Define Variables
database = os.path.dirname(os.path.abspath(__file__)) +  "/aprsnotify.db"

# Define Functions
def clear_screen(): # Defines function to clear the screen to make output easier to read
    if name == 'nt': # windows
        _ = system('cls')
    else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
        _ = system('clear')

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def run_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def select_sql(conn, sql):
    # Executes SQL for Selects - Returns a "value"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

## Main Program

conn = create_connection(database)

ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]

if version < 5.0:

    # Install new Dependenacies
    os.system("pip3 install discord-webhook")
    os.system("pip3 install matterhook")

    # Add new columns to database
    sql = """
    Alter table apikeys add discord_webhook_url text null;
    """
    run_sql(conn, sql)

    sql = """
    Alter table apikeys add mattermost_webhook_url text null;
    """
    run_sql(conn, sql)

    sql = """
    Alter table config add send_to_discord int;
    """
    run_sql(conn, sql)

    sql = """
    Alter table config add send_to_mattermost int;
    """
    run_sql(conn, sql)

    sql = """
    update config set send_to_discord = 0;
    """
    run_sql(conn, sql)

    sql = """
    update config set send_to_mattermost = 0;
    """
    run_sql(conn, sql)

    sql = """ create table if not exists callsignlists (
    callsign text null,
    listtype text null
    ); """

    run_sql(conn, sql)

    sql = """insert into callsignlists (callsign, listtype) 
    select callsign, 'POS' from pos_callsigns
    union
    select callsign, 'MSG' from msg_callsigns
    union
    select callsign, 'WX' from wx_callsigns;
    """

    run_sql(conn, sql)

    sql = """drop table pos_callsigns;"""

    run_sql(conn, sql)

    sql = """drop table msg_callsigns;"""

    run_sql(conn, sql)

    sql = """drop table wx_callsigns;"""

    run_sql(conn, sql)

    sql = """drop table anutilmenu;"""

    run_sql(conn, sql)

    sql = """drop view vw_config_menu;"""

    run_sql(conn, sql)

    sql = "update config set version = 5.0;"

    run_sql(conn, sql)

    checksendtoall = select_sql(conn,"select send_to_all from config")

    if checksendtoall[0][0] == 1:
        sql = "update config set "
        sql = sql + "send_to_twitter = 1, "
        sql = sql + "send_to_telegram = 1, "
        sql = sql + "send_to_mastodon = 1;"

        run_sql(conn, sql)

ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]

if version == 5.0:

    # Perform Table Updates
    sql = "alter table apikeys add mm_wh_api_key text null;"
    run_sql(conn, sql)

    sql = "update config set version = 5.1;"
    run_sql(conn, sql)

ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]

if version == 5.1:

    # Install new Dependenacies

    # Perform Table Updates

    sql = "alter table apikeys rename discord_webhook_url to discord_poswx_wh_url;"
    run_sql(conn, sql)

    sql = "alter table apikeys add discord_aprsmsg_wh_url text null;"
    run_sql(conn, sql)  

    sql = "alter table apikeys add pushover_token text null;"
    run_sql(conn, sql)  

    sql = "alter table apikeys add pushover_userkey text null;"
    run_sql(conn, sql)  

    sql = """
        create table config_new (
        twitter boolean,
        telegram boolean,
        mastodon boolean,
        discord boolean,
        mattermost boolean,
        units_to_use int,
        include_map_image_telegram boolean,
        include_wx boolean,
        send_position_data boolean,
        send_weather_data boolean,
        aprsmsg_notify_telegram boolean,
        aprsmsg_notify_discord boolean,
        enable_aprsmsg_notify boolean,
        aprsmsg_notify_pushover boolean,
        version float
        ); """

    run_sql(conn, sql) 

    sql = """
    insert into config_new (twitter, telegram, mastodon, discord, mattermost, units_to_use, include_map_image_telegram, include_wx, send_position_data, send_weather_data, aprsmsg_notify_telegram, aprsmsg_notify_discord, enable_aprsmsg_notify, aprsmsg_notify_pushover, version)
    select 
    case when send_to_twitter = 1 then True else False END as twitter,
    case when send_to_telegram = 1 then True else False END as telegram,
    case when send_to_mastodon = 1 then True else False END as mastodon,
    case when send_to_discord = 1 then True else False END as discord,
    case when send_to_mattermost = 1 then True else False END as mattermost,
    units_to_use,
    case when include_map_image = 1 then True else False END as include_map_image_telegram,
    case when include_wx = 1 then True else False END as include_wx,
    case when send_position_data = 1 then True else False END as send_position_data,
    case when send_weather_data = 1 then True else False END as send_weather_data,
    case when enable_aprs_msg_notify = 1 then True else False END as aprsmsg_notify_telegram,
    False as aprsmsg_notify_discord,
    False as enable_aprsmsg_notify,
    False as aprsmsg_notify_pushover,
    version
    from config;

    """
    run_sql(conn, sql)

    sql = "drop table config;"
    run_sql(conn, sql)

    sql = "alter table config_new rename to config;"    
    run_sql(conn, sql)

   

    sql = "update config set version = 6.0;"
    run_sql(conn, sql)

ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]

if version == 6.0:

    # Install new Dependenacies

    # Perform Table Updates

    sql = """
        create table config_new (
        twitter boolean,
        telegram boolean,
        mastodon boolean,
        discord boolean,
        mattermost boolean,
        slack boolean,
        units_to_use int,
        include_map_image_telegram boolean,
        include_wx boolean,
        send_position_data boolean,
        send_weather_data boolean,
        aprsmsg_notify_telegram boolean,
        aprsmsg_notify_discord boolean,
        aprsmsg_notify_pushover boolean,
        aprsmsg_notify_slack boolean,
        aprsmsg_notify_mattermost boolean,
        club_telegram boolean,
        club_discord boolean,
        club_mattermost boolean,
        club_slack boolean,
        version text
        ); """

    run_sql(conn, sql) 

    sql = """
    insert into config_new (twitter, telegram, mastodon, discord, mattermost, slack, units_to_use, include_map_image_telegram, include_wx, send_position_data, send_weather_data, 
    aprsmsg_notify_telegram, aprsmsg_notify_discord, aprsmsg_notify_pushover, aprsmsg_notify_slack, aprsmsg_notify_mattermost, club_telegram, club_discord, club_mattermost, 
    club_slack, version)

    select 
    twitter,
    telegram,
    mastodon,
    discord,
    mattermost,
    False as slack,
    units_to_use,
    include_map_image_telegram,
    include_wx,
    send_position_data,
    send_weather_data,
    aprsmsg_notify_telegram,
    aprsmsg_notify_discord,
    aprsmsg_notify_pushover,
    False as aprsmsg_notify_slack,
    False as aprsmsg_notify_mattermost,
    False as club_telegram,
    False as club_discord,
    False as club_mattermost,
    False as club_slack,
    0 as version
    from config;

    """
    run_sql(conn, sql)

    sql = "drop table config;"
    run_sql(conn, sql)

    sql = "alter table config_new rename to config;"    
    run_sql(conn, sql)

    sql = "alter table apikeys add slack_aprsmsg_wh_url text null;"
    run_sql(conn, sql)  

    sql = "alter table apikeys add slack_poswx_wh_url text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys rename mattermost_webhook_url to mattermost_poswx_wh_url;"
    run_sql(conn, sql)

    sql = "alter table apikeys rename mm_wh_api_key to mattermost_poswx_api_key;"
    run_sql(conn, sql)

    sql = "alter table apikeys add mattermost_aprsmsg_wh_url text null;"
    run_sql(conn, sql)  

    sql = "alter table apikeys add mattermost_aprsmsg_api_key text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys rename telegram_my_chat_id to telegram_poswx_chat_id;"
    run_sql(conn, sql)

    sql = "alter table apikeys add telegram_aprsmsg_chat_id text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys add telegram_club_chat_id text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys add telegram_club_bot_token text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys add discord_club_wh_url text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys add mattermost_club_wh_url text null;"
    run_sql(conn, sql)  

    sql = "alter table apikeys add mattermost_club_api_key text null;"
    run_sql(conn, sql) 

    sql = "alter table apikeys add slack_club_wh_url text null;"
    run_sql(conn, sql) 

    sql = "update config set version = '01202022';"
    run_sql(conn, sql)

ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]

if version == '01202022':
    
    # Drop Twitter columns from config table
    sql = """
        create table config_new (
        telegram boolean,
        mastodon boolean,
        discord boolean,
        mattermost boolean,
        slack boolean,
        units_to_use int,
        include_map_image_telegram boolean,
        include_wx boolean,
        send_position_data boolean,
        send_weather_data boolean,
        aprsmsg_notify_telegram boolean,
        aprsmsg_notify_discord boolean,
        aprsmsg_notify_pushover boolean,
        aprsmsg_notify_slack boolean,
        aprsmsg_notify_mattermost boolean,
        club_telegram boolean,
        club_discord boolean,
        club_mattermost boolean,
        club_slack boolean,
        version text
        ); """

    run_sql(conn, sql) 

    sql = """
    insert into config_new (telegram, mastodon, discord, mattermost, slack, units_to_use, include_map_image_telegram, include_wx, send_position_data, send_weather_data, 
    aprsmsg_notify_telegram, aprsmsg_notify_discord, aprsmsg_notify_pushover, aprsmsg_notify_slack, aprsmsg_notify_mattermost, club_telegram, club_discord, club_mattermost, 
    club_slack, version)

    select 
    telegram,
    mastodon,
    discord,
    mattermost,
    False as slack,
    units_to_use,
    include_map_image_telegram,
    include_wx,
    send_position_data,
    send_weather_data,
    aprsmsg_notify_telegram,
    aprsmsg_notify_discord,
    aprsmsg_notify_pushover,
    False as aprsmsg_notify_slack,
    False as aprsmsg_notify_mattermost,
    False as club_telegram,
    False as club_discord,
    False as club_mattermost,
    False as club_slack,
    0 as version
    from config;

    """
    run_sql(conn, sql)

    sql = "drop table config;"
    run_sql(conn, sql)

    sql = "alter table config_new rename to config;"    
    run_sql(conn, sql)

    # Drop twitter columns from API Keys table

    sql = """
        create table apikeys_new (
        telegram_bot_token text null,
        telegram_poswx_chat_id text null,
        aprsfikey text null,
        openweathermapkey text null,
        mastodon_client_id text null,
        mastodon_client_secret text null,
        mastodon_api_base_url text null,
        mastodon_user_access_token text null,
        discord_poswx_wh_url text null,
        mattermost_poswx_wh_url text null,
        discord_aprsmsg_wh_url text null,
        pushover_token text null,
        pushover_userkey text null,
        slack_aprsmsg_wh_url text null,
        slack_poswx_wh_url text null,
        mattermost_poswx_api_key text null,
        mattermost_aprsmsg_wh_url text null,
        mattermost_aprsmsg_api_key text null,
        telegram_aprsmsg_chat_id text null,
        telegram_club_chat_id text null,
        telegram_club_bot_token text null,
        discord_club_wh_url text null,
        mattermost_club_wh_url text null,
        mattermost_club_api_key text null,
        slack_club_wh_url text null
        ); """

    run_sql(conn, sql) 

    sql = """
    insert into apikeys_new (telegram_bot_token, telegram_my_chat_id, aprsfikey, openweathermapkey, discord_poswx_wh_url, mattermost_webhook_url, discord_aprsmsg_wh_url,
   pushover_token, pushover_userkey, slack_aprsmsg_wh_url, slack_poswx_wh_url, mattermost_poswx_api_key,
   mattermost_aprsmsg_wh_url,
   mattermost_aprsmsg_api_key,
   telegram_aprsmsg_chat_id,
      telegram_club_chat_id,
   telegram_club_bot_token,
   discord_club_wh_url,
   mattermost_club_wh_url,
   mattermost_club_api_key,
   slack_club_wh_url)

    select 
telegram_bot_token, telegram_my_chat_id, aprsfikey, openweathermapkey, discord_poswx_wh_url, mattermost_webhook_url, discord_aprsmsg_wh_url,
   pushover_token, pushover_userkey, slack_aprsmsg_wh_url, slack_poswx_wh_url, mattermost_poswx_api_key,
   mattermost_aprsmsg_wh_url,
   mattermost_aprsmsg_api_key,
   telegram_aprsmsg_chat_id,
      telegram_club_chat_id,
   telegram_club_bot_token,
   discord_club_wh_url,
   mattermost_club_wh_url,
   mattermost_club_api_key,
   slack_club_wh_url
   from apikeys;

    """
    run_sql(conn, sql)

    sql = "drop table apikeys;"
    run_sql(conn, sql)

    sql = "alter table apikeys_new rename to apikeys;"    
    run_sql(conn, sql)

    sql = "update config set version = '02032023';"
    run_sql(conn, sql)



