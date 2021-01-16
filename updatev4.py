# Import libraries
import sqlite3
import config
import os
import pickle
from os import system, name
from sqlite3 import Error
from mastodon import Mastodon

# Define Variables
version = 4.0
config_fname = "config"
config_old = config_fname + ".old"
configfile = config_fname + ".py"
database = os.path.dirname(os.path.abspath(__file__)) +  "/aprsnotify.db"
locdtstampfile = os.path.dirname(os.path.abspath(__file__)) + "/locdtstamp.txt"
linefeed = "\n"
linebreak = "------------------------------------------------------"
title_line = "APRSNotify Version " + version + " Update Utility"
send_to_all = 0
send_to_twitter = 0
send_to_telegram = 0
send_to_mastodon = 0


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

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)    

def run_sql(conn,sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


# Main Program

# build database

create_config_table = """ create table if not exists config (
    send_to_all int,
    send_to_twitter int,
    send_to_telegram int,
    send_to_mastodon int,
    units_to_use int,
    enable_aprs_msg_notify int,
    include_map_image int,
    include_wx int,
    send_position_data int,
    send_weather_data int,
    version float
); """

create_aprsstamps_table = """ create table if not exists aprsstamps (
    lastpostime int,
    lastmsgid int,
    lastwxtime int
); """

create_poscallsign_table = """ create table if not exists pos_callsigns (
    callsign text null
); """

create_msgcallsign_table = """ create table if not exists msg_callsigns (
    callsign text null
); """

create_wxcallsign_table = """ create table if not exists wx_callsigns (
    callsign text null
); """

create_apikeys_table = """ create table if not exists apikeys (
    twitter_consumer_key text null,
    twitter_consumer_secret text null,
    twitter_access_token text null,
    twitter_access_secret text null,
    telegram_bot_token text null,
    telegram_my_chat_id text null,
    aprsfikey text null,
    openweathermapkey text null,
    mastodon_client_id text null,
    mastodon_client_secret text null,
    mastodon_api_base_url text null,
    mastodon_user_access_token text null
); """

create_anutilmenu_table =  """ create table if not exists anutilmenu (
    menu_id int,
    submenu_id int,
    menu_item text null
    );"""

create_view_configmenu = """
create view vw_config_menu as
select 
    menu_id, 
	menu_item,
	case (select send_to_all from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 1
UNION
select
    menu_id, 
	menu_item,
	case (select send_to_twitter from config) 
			when 0 then 'OFF'
			else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 2
UNION
select
    menu_id, 
	menu_item,
	case (select send_to_telegram from config)
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 3
UNION
select
    menu_id, 
	menu_item,
	case (select send_to_mastodon from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 4 
UNION
select
    menu_id, 
	menu_item,
	case (select units_to_use from config)
		when 1 then 'METRIC'
		else 'IMPERIAL'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 5
UNION
select
    menu_id, 
	menu_item,
	case (select enable_aprs_msg_notify from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 6
UNION
select
    menu_id, 
	menu_item,
	case (select include_map_image from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 7
UNION
select
    menu_id, 
	menu_item,
	case (select include_wx from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 8
UNION
select
    menu_id, 
	menu_item,
	case (select send_position_data from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 9
UNION
select
    menu_id, 
	menu_item,
	case (select send_weather_data from config) 
		when 0 then 'OFF'
		else 'ON'
		end as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 10
UNION
select
    menu_id, 
	menu_item,
    null as current_state
    from anutilmenu where submenu_id = 5
	and menu_id = 11;

"""

conn = create_connection(database)

create_table(conn, create_config_table)
create_table(conn, create_aprsstamps_table)
create_table(conn, create_poscallsign_table)
create_table(conn, create_msgcallsign_table)
create_table(conn, create_wxcallsign_table)
create_table(conn, create_apikeys_table)
create_table(conn, create_anutilmenu_table)
create_table(conn, create_view_configmenu)

# insert data

if 0 in config.send_status_to:
    send_to_all = 1
if 1 in config.send_status_to:
    send_to_twitter = 1
if 2 in config.send_status_to:
    send_to_telegram = 1
if 3 in config.send_status_to:
    send_to_mastodon = 1

sql = """insert into config (send_to_all, send_to_twitter, send_to_telegram, send_to_mastodon, units_to_use, enable_aprs_msg_notify, 
    include_map_image, include_wx, send_position_data, send_weather_data, version)
    values (""" 

sql = sql + str(send_to_all) + ", "   
sql = sql + str(send_to_twitter) + ", " 
sql = sql + str(send_to_telegram) + ", "
sql = sql + str(send_to_mastodon) + ", " 
sql = sql + str(config.units_to_use) + ", "
sql = sql + str(config.enable_aprs_msg_notify) + ", "
sql = sql + str(config.include_map_image) + ", "
sql = sql + str(config.include_wx) + ", "
sql = sql + "1,0," + version + ");"

run_sql(conn,sql)

sql = """insert into apikeys (twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret,
    telegram_bot_token, telegram_my_chat_id, aprsfikey, openweathermapkey)
    values('"""
sql = sql + config.twitterkeys["consumer_key"] + "', "
sql = sql + "'" + config.twitterkeys["consumer_secret"] + "', "
sql = sql + "'" + config.twitterkeys["access_token"] + "', "
sql = sql + "'" + config.twitterkeys["access_secret"] + "', "
sql = sql + "'" + config.telegramkeys["my_bot_token"] + "', "
sql = sql + "'" + config.telegramkeys["my_chat_id"] + "', "
sql = sql + "'" + config.aprsfikey + "', "
sql = sql + "'" + config.openweathermapkey + "');"

run_sql(conn,sql)

sql = """
insert into anutilmenu (menu_id, submenu_id, menu_item)
    values
    (1,1,'Work with Social Media API Keys'),
    (2,1,'Update Other API Keys'),
    (3,1,'Work with Callsign Lists'),
    (4,1,'Change configuration settings'),
    (5,1,'Exit Utility'),
    (1,3,'Twitter API Keys'),
    (2,3,'Telegram API Keys'),
    (3,3,'Mastodon API Keys'),
    (4,3,'Return to Main Menu'),
    (1,6,'Update Consumer Key'),
    (2,6,'Update Consumer Secret'),
    (3,6,'Update Access Token'),
    (4,6,'Update Access Secret'),
    (5,6,'Return to Main Menu'),
    (1,7,'Update My Bot Token'),
    (2,7,'Update Chat ID'),
    (3,7,'Return to Main Menu'),
    (1,8,'Obtain New Keys (Only needed if moving instances/accounts)'),
    (2,8,'Return to Main Menu'),
    (1,5,'Toggle Send to All Social Media (Turn On/Off)'),
    (2,5,'Toggle Send to Twitter (Turn On/Off)'),
    (3,5,'Toggle Send to Telegram (Turn On/Off)'),
    (4,5,'Toggle Send to Mastodon (Turn On/Off)'),
    (5,5,'Toggle Units To Use (Imperial/Metric)'),
    (6,5,'Toggle APRS Message Notification (Turn On/Off)'),
    (7,5,'Toggle Include Map Image to Telegram (Turn On/Off)'),
    (8,5,'Toggle Include Weather in Status (Turn On/Off)'),
    (9,5,'Toggle send position data (Turn On/Off)'),
    (10,5,'Toggle send Weather Data (Turn On/Off)'),
    (11,5,'Return to Main Menu'),
    (1,9,'Add POS Callsign to list'),
    (2,9,'Delete POS Callsign from list'),
    (3,9,'Add MSG Callsign to list'),
    (4,9,'Delete MSG Callsign from list'),
    (5,9,'Add WX Callsign to list'),
    (6,9,'Delete WX Callsign from list'),
    (7,9,'Return to Main Menu'),
    (1,11,'Update APRS.fi Key'),
    (2,11,'Update Openweathermap API Key'),
    (3,11,'Return to Main Menu');
"""
run_sql(conn,sql)

with open(locdtstampfile,"rb") as f:
    chks = pickle.load(f)
    f.close()

# - insert values from locdtstamp.txt here.

sql = """insert into aprsstamps (lastpostime, lastmsgid)
    values("""
sql = sql + str(chks["lasttime"]) + ", "
sql = sql + str(chks["lastmsgid"]) + ", "
sql = sql + str(1) + ");"

run_sql(conn,sql)


##################################################################

clear_screen() # Clears the screen to make output easier to read

msg = title_line + """

PLEASE READ THIS FIRST!

Welcome to the APRSNotify Version 4.0 Update Utility. 

This utility will update your version of the configuration file for APRSNotify.

With Version 4.0 we have now moved from a config.py file and the locdtstamp.txt file to store data in and are now
running an SQLite3 database to store configuration and reference data. 

Luckly, I have been able to bring in most of your original config.py file and whatever data is stored in the locdtstamp.txt file,
however, I do need some final help from you. After hitting enter, you will be asked to set a few more variables.

When this utility is finished, the old config.py file will be renamed to config.old in case you ever want to reference it in the future.

If you need to access the database to make changes to the configuration in the future, please run the anutil.py file and it will walk you through
what is needed to make updates.
""" + linefeed + linefeed

print(msg)

pause = input("When you are ready to continue, please press enter.")
#-----------------------------------------

clear_screen() # Clears the screen to make output easier to read

msg = title_line + """

First we need to re-enter the list of callsigns to track for position data. Because of differences in how the list was stored between Ver 3.1 and earlier versions,
it is harder for me to bring this list in automatically.

Please enter the list below of callsigns in the following format:

callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

Note that there is a max of 20 callsigns that can be entered. Any more than 20 will be cut off.


"""

print(msg)

pos_callsignlist = list(map(str,input("Callsign List: ").split(',')))

if config.enable_aprs_msg_notify == 1:
    msg = """

Since you were using APRS Message Notification in the old version, we now need to do the same for the ID's that you want to monitor
for messages. 

Please enter the list below of callsigns in the following format:

callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

Note that there is a max of 10 callsigns that can be entered. Any more than 10 will be cut off.

"""

    print(msg)

    msg_callsignlist = list(map(str,input("Callsign List: ").split(',')))

    if len(pos_callsignlist) < 20:
        pos_calllistlen = len (pos_callsignlist)
    else:
        pos_calllistlen = 20

    for i in range(0,pos_calllistlen):
        sql = """insert into pos_callsigns (callsign)
        values("""
        sql = sql + "'" + pos_callsignlist[i].upper().strip() + "');"

        run_sql(conn,sql)

    if len(msg_callsignlist) < 10:
        msg_calllistlen = len (msg_callsignlist)
    else:
        msg_calllistlen = 20

    for i in range(0,msg_calllistlen):
        sql = """insert into msg_callsigns (callsign)
        values("""
        sql = sql + "'" + msg_callsignlist[i].upper().strip() + "');"

        run_sql(conn,sql)

#-----------------------------------------

clear_screen() # Clears the screen to make output easier to read

msg = title_line + """
Do you have an APRS Station that is sending weather data to the APRS network? If so, we can pull that data and 
parse it and send it to Social Media as well."""

while True:
    send_weather_status = int(input("Would you like to send the parsed Weather Data to Social Media (Y/N): "))
    if send_weather_status.upper().strip() == 'Y' or send_weather_status.upper().strip() == 'N':
        break

if send_weather_status.upper().strip() == 'Y':

    msg = """

    Then we need yout to enter the list of the callsign(s) of the weather station(s) you want to track.

    Please enter the list below of callsigns in the following format:

    callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

    Note that there is a max of 20 callsigns that can be entered. Any more than 20 will be cut off.


    """

    print(msg)

    wx_callsignlist = list(map(str,input("Callsign List: ").split(',')))

    if len(wx_callsignlist) < 20:
        wx_calllistlen = len (wx_callsignlist)
    else:
        wx_calllistlen = 20

    for i in range(0,wx_calllistlen):
        sql = """insert into pos_callsigns (callsign)
        values("""
        sql = sql + "'" + wx_callsignlist[i].upper().strip() + "');"

        run_sql(conn,sql)


########################################

clear_screen() # Clears the screen to make output easier to read

msg = title_line + """

A new feature that has been added to Version 4.0 is the ability to not only send to Twitter and Telegram, but also now to Mastodon. 

Mastodon is decentralized social network that looks and functions like Twitter, but is decentralized and federated and runs on multiple instances.

For more information, you can search for Mastodon, or go to: https://joinmastodon.org/.

If you are already using Mastodon, then you know what it is and how it works.

In order for the Mastodon bot to work, you will need to have created a new account on an instance as described in the README section on getting the Mastodon API keys. 

In order to retrieve those keys for you, I need you to provide me with some informtion. Please note, I will be asking for your username and password. This is only used to create 
an app and retrieve the keys needed for APRSNotify to post as your bot account. I DO NOT STORE THE USERNAME AND PASSWORD ONCE THE KEYS HAVE BEEN GENERATED. Once the keys are created, I use 
those to connect to the bot/instance, so your username and password are safe.

"""

print(msg)

use_mastodon = input("Would you like to send your status to a Mastodon Bot knowing this information? (Y/N): ")

if use_mastodon.upper() == 'Y':
    clear_screen() # Clears the screen to make output easier to read

    msg = title_line + """

MASTODON CONFIGURATION

Alright then let's start gathering the information we need to generate these Mastodon Keys.

"""

    print(msg)

    mastodon_instance_url = input("First, I need the url of the instance your bot account is on (EX: https://botsin.space): ")
    mastodon_bot_app_name = input("Now I need to know what you want to call the app. Make it unique (EX: my_aprs_bot): ")
    mastodon_username = input("Now I need the username for the bot account: ")
    mastodon_password = input("Finally I need the password for the bot account: ")

    client_keys = Mastodon.create_app(mastodon_bot_app_name, scopes=['read', 'write'], api_base_url=mastodon_instance_url)

    mastodon_api = Mastodon(client_keys[0], client_keys[1], api_base_url = mastodon_instance_url)

    access_token = mastodon_api.log_in(mastodon_username, mastodon_password, scopes=["read", "write"])

    sql = """insert into apikeys (mastodon_client_id, mastodon_client_secret,mastodon_api_base_url,mastodon_user_access_token)
    values('"""

    sql = sql + client_keys[0] + "','"
    sql = sql + client_keys[1] + "','"
    sql = sql + mastodon_instance_url + "','"
    sql = sql + access_token + "');"

    run_sql(conn,sql)

    msg = """

    Your Mastodon keys have been generated and stored in the database. If you need to retrieve them, please use the an_util.py script."""

    print(msg)

########################################

clear_screen() # Clears the screen to make output easier to read

msg = title_line + linebreak + """

Thank you for updating to the newest version of APRSNotify. Hope you enjoy the new features. If you need to make future adjustments or retrieve informtation from the database,
please use the an_util.py script in the APRSNotify folder.

"""

print(msg)

pause = input("When you are ready to continue, please press enter.")

clear_screen()