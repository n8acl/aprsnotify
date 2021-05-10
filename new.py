# Setup script for APRSNotify

def setup(conn):
    import sqlite3
    import os
    import sys
    from os import system, name
    from sqlite3 import Error
    from mastodon import Mastodon

    # Define Static Variables
    version = 4.0
    linefeed = "\n"
    linebreak = "------------------------------------------------------"
    title_line = "APRSNotify Configuration Setup Utility"
    send_to_all = -1
    send_to_twitter = -1
    send_to_telegram = -1
    send_to_mastodon = -1
    units_to_use = -1
    enable_aprs_msg_notify = -1
    include_map_image = -1
    include_wx = - 1
    send_staus_types = -1

    # Define Functions
    def clear_screen(): # Defines function to clear the screen to make output easier to read
        if name == 'nt': # windows
            _ = system('cls')
        else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
            _ = system('clear')

    def get_services(arg):
        
        switcher = {
            0: "All",
            1: "Twitter",
            2: "Telegram",
            3: "Mastodon"
        }
        return switcher.get(arg,"Nothing")

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

    def set_twitter_keys(conn):
        msg = "In order to use Twitter, You will need to obtain 4 API Keys from them: consumer_key, consumer_secret, access_token, access_secret " + linefeed + linefeed
        print(msg)
        consumer_key = input("Please copy and paste your consumer_key here: ")
        consumer_secret = input("Please copy and paste your consumer_secret here: ")
        access_token = input("Please copy and paste your access_token here: ")
        access_secret = input("Please copy and paste your access_secret here: ")
        print(linefeed)

        sql = "update apikeys set twitter_consumer_key = '" + consumer_key +"', "
        sql = sql + "twitter_consumer_secret = '" + consumer_secret + "', "
        sql = sql + "twitter_access_token = '" + access_token + "', "
        sql = sql + "twitter_access_secret = '" + access_secret + "';"

        run_sql(conn, sql)
        
        sql = "update config set twitter_consumer_key = '" + consumer_key +"', "
        sql = sql + "twitter_consumer_secret = '" + consumer_secret + "', "
        sql = sql + "twitter_access_token = '" + access_token + "', "
        sql = sql + "twitter_access_secret = '" + access_secret + "';"

        run_sql(conn, sql)

    def set_telgram_keys(conn):
        msg = "In order to use Telegram, You will need to obtain 2 Keys from them: The Bot Token and Your Chat ID " + linefeed + linefeed
        print(msg)
        my_bot_token = input("Please copy and paste your Bot Token here: ")
        my_chat_id = input("Please copy and paste your Chatid here: ")
        print(linefeed)

        sql = "update apikeys set telegram_bot_token = '" + my_bot_token +"', "
        sql = sql + "telegram_my_chat_id = '" + my_chat_id + "';"

        run_sql(conn, sql)

    def set_mastodon_keys(conn):
        msg = "In order to use Mastodon, we need to and can generate the keys here." + linefeed + linefeed
        print(msg)

        mastodon_instance_url = input("First, I need the url of the instance your bot account is on (EX: https://botsin.space): ")
        mastodon_bot_app_name = input("Now I need to know what you want to call the app. Try to make it unique (EX: my_aprs_bot): ")
        mastodon_username = input("Now I need the username for the bot account: ")
        mastodon_password = input("Finally I need the password for the bot account: ")

        client_keys = Mastodon.create_app(mastodon_bot_app_name, scopes=['read', 'write'], api_base_url=mastodon_instance_url)
        client_id = client_keys[0]
        client_secret = client_keys[1]

        mastodon_api = Mastodon(client_id, client_secret, api_base_url = mastodon_instance_url)

        access_token = mastodon_api.log_in(mastodon_username, mastodon_password, scopes=["read", "write"])

        sql = "update apikeys set mastodon_client_id = '" + client_id + "', "
        sql = sql + "mastodon_client_secret = '" + client_secret + "', "
        sql = sql + "mastodon_api_base_url = '" + mastodon_instance_url + "', "
        sql = sql + "mastodon_user_access_token = '" + access_token + "';"
        
        run_sql(conn,sql)


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

    create_table(conn, create_config_table)
    create_table(conn, create_aprsstamps_table)
    create_table(conn, create_poscallsign_table)
    create_table(conn, create_msgcallsign_table)
    create_table(conn, create_wxcallsign_table)
    create_table(conn, create_apikeys_table)
    create_table(conn, create_anutilmenu_table)
    create_table(conn, create_view_configmenu)

    sql = """insert into config (send_to_all, send_to_twitter, send_to_telegram, send_to_mastodon, units_to_use, enable_aprs_msg_notify, 
    include_map_image, include_wx,send_position_data, send_weather_data, version)
    values (0,0,0,0,0,0,0,0,0,0,""" + str(version) + """);"""

    run_sql(conn,sql)

    sql = """insert into apikeys (twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret,
    telegram_bot_token, telegram_my_chat_id, aprsfikey, openweathermapkey)
    values(null,null,null,null,null,null,null,null);"""

    run_sql(conn_sql)

    sql = """insert into aprsstamps (lastpostime, lastmsgid)
    values(1,1,1);
    """ 
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



    #################

    clear_screen() # Clears the screen to make output easier to read

    msg = title_line + """

    PLEASE READ THIS FIRST!

    Welcome and thank you for using APRSNotify. This first run utility will help you to configure the database for the script. 

    Please follow the directions found in the wiki at https://github.com/n8acl/aprsnotify in order to obtain the 
    API keys you will need for this script.

    If this changes need to be made again in the future, please run an_util.py to interact with the database.
    
    """ + linefeed + linefeed

    print(msg)

    pause = input("When you are ready to continue, please press enter.")
    #-----------------------------------------

    clear_screen() # Clears the screen to make output easier to read

    msg = title_line 

    print(msg)

    msg = ""

    msg = msg + """

    First we need to choose and configure the Social Media service(s) you plan to use. 
    
    To start off with, would you like to send to All the services? This would be Twitter, Telegram and Mastodon.

    0 = No
    1 = Yes

    """
    print(msg)

    while True:
        send_to_all = int(input("Please enter your selection: "))
        if (send_to_all == 1 or send_to_all == 0):
            break
    
    if send_to_all == 1:
        sql = "update config set send_to_all = 1;"
        run_sql(conn,sql)

        print(linefeed)
        set_twitter_keys(conn)
        print(linefeed)
        set_telegram_keys(conn)
        print(linefeed)
        set_mastodon_keys(conn)
    else:
        clear_screen() # Clears the screen to make output easier to read

        msg = title_line 

        print(msg)

        msg = ""

        msg = msg + """

        Since you said no to using all available services, let's find the ones you want to use.

        Do you want to send to Twitter?

        0 = No
        1 = Yes

        """
        print(msg)

        while True:
            send_to_twitter = int(input("Please enter your selection: "))
            if (send_to_twitter == 1 or send_to_twitter == 0):
                break

        if send_to_twitter == 1:
            sql = "update config set send_to_twitter = 1;"
            run_sql(conn,sql)

            print(linefeed)
            set_twitter_keys(conn)
        
        ##################

        clear_screen() # Clears the screen to make output easier to read

        msg = title_line 

        print(msg)

        msg = ""

        msg = msg + """

        Do you want to send to Telegram? 
        Note: If you wish to use APRS Message Notifications, you will need Telegram Bot Keys.

        0 = No
        1 = Yes

        """
        print(msg)

        while True:
            send_to_telegram = int(input("Please enter your selection: "))
            if (send_to_telegram == 1 or send_to_telegram == 0):
                break

        if send_to_telegram == 1:
            sql = "update config set send_to_telegram = 1;"
            run_sql(conn,sql)

            print(linefeed)
            set_telegram_keys(conn)

        ##################

        clear_screen() # Clears the screen to make output easier to read

        msg = title_line 

        print(msg)

        msg = ""

        msg = msg + """

        Do you want to send to Mastodon? 
        
        0 = No
        1 = Yes

        """
        print(msg)

        while True:
            send_to_mastodon = int(input("Please enter your selection: "))
            if (send_to_mastodon == 1 or send_to_mastodon == 0):
                break

        if send_to_mastodon == 1:
            sql = "update config set send_to_mastodon = 1;"
            run_sql(conn,sql)

            print(linefeed)
            set_mastodon_keys(conn)

    #-----------------------------------------
    clear_screen()

    msg = title_line + """

    What kind of statuses do you want to sent to Social Media?
    You have the choice of sending just Position Data or, if you have a weather station sending data to the ARPS network,
    this script can parse that data and send it in it's own status update. 

    1 = Send both Position and Weather Data
    2 = Send just Positiion Data
    3 = Send just Weather Data
    """
    print(msg)

    status_types = [1,2,3]

    while True:
        send_status_types = int(input("Enter the number for the units you want to use: "))
        if send_status_types in status_types:
            break
    
    if send_status_types == 1:
        sql = "update config set send_position_data = 1, send_weather_data = 1;"
    if send_status_types == 2:
        sql = "update config set send_position_data = 1, send_weather_data = 0;"
    else:
        sql = "update config set send_position_data = 0, send_weather_data = 1;"
    run_sql(conn,sql)

    #-----------------------------------------
    clear_screen()

    msg = title_line + """

    What type of units of measure do you want to use?

    1 = Metric (Celcius, Kilometers Per Hour, Etc)
    2 = Imperial (Farenheit, Miles Per Hour, Etc)
    """
    print(msg)

    while True:
        units_to_use = int(input("Enter the number for the units you want to use: "))
        if (units_to_use == 1 or units_to_use == 2):
            break
    
    sql = "update config set units_to_use = " + units_to_use + ";"
    run_sql(conn,sql)


    #-----------------------------------------
    if (send_to_all == 1 or send_to_telegram == 1): 

        clear_screen()

        msg = title_line + """

    Since you indicated earlier that you are using Telegram, you could use APRS message notification if you want.
    If someone sends a messsage to one of the callsigns being tracked by this script, the script will send you a notification
    on Telegram. You would also be able to send messages from Telegram to APRS as well if you are using the APRSBot companion script.

    Do you want to enable or disable APRS message notification?

    0 = Disable
    1 = Enable
        """
        print(msg)

        while True:
            enable_aprs_msg_notify = int(input("Enter the number for you choice: "))
            if (enable_aprs_msg_notify == 1 or enable_aprs_msg_notify == 0):
                break

        sql = "update config set enable_aprs_msg_notify = " + enable_aprs_msg_notify + ";"
        run_sql(conn,sql)        

        #-----------------------------------------
        clear_screen()

        msg = title_line + """

    Do you want to include a map image on your Telegram posts?

    0 = No
    1 = Yes
        """
        print(msg)

        while True:
            include_map_image = int(input("Enter the number for your choice: "))
            if (include_map_image == 1 or include_map_image == 0):
                break

        sql = "update config set include_map_image = " + include_map_image + ";"
        run_sql(conn,sql)  
    #-----------------------------------------
    clear_screen()

    msg = title_line + """

    Also, do you want to include a weather report in your statuses? This is the Temp and conditions at the location of the APRS Packet.
    Note that this will require an API key from OpenWeatherMap at https://openweathermap.org/api to work. 

    0 = Disable
    1 = Enable
    """
    print(msg)

    while True:
        include_wx = int(input("Enter the number of your choice: "))
        if (include_wx == 1 or include_wx == 0):
            break

    sql = "update config set include_wx = " + include_wx + ";"
    run_sql(conn,sql) 
    #-----------------------------------------
    clear_screen()

    msg = title_line +"""

    Now we have the last few things we need to configure for the script.
    
    First we need to enter the list of callsigns to track for position data.

    Please enter the list below of callsigns in the following format, seperated by commas:

    callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

    Note that there is a max of 20 callsigns that can be entered. Any more than 20 will be cut off.


    """

    print(msg)

    pos_callsignlist = list(map(str,input("Callsign List: ").split(',')))

    if len(pos_callsignlist) < 20:
        pos_calllistlen = len(pos_callsignlist)
    else:
        pos_calllistlen = 20

    for i in range(0,pos_calllistlen):
        sql = """insert into pos_callsigns (callsign)
        values("""
        sql = sql + "'" + pos_callsignlist[i].upper().strip() + "');"

        run_sql(conn,sql)


    if enable_aprs_msg_notify == 1:
        msg = """

    Since you indicated you want to use message notification, we now need to do the same for the ID's that you want to monitor
    for messages. 

    Please enter the list below of callsigns in the following format, seperated by commas:

    callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

    Note that there is a max of 10 callsigns that can be entered. Any more than 10 will be cut off.

    """

        print(msg)

        msg_callsignlist = list(map(str,input("Callsign List: ").split(',')))
        if len(msg_callsignlist) < 10:
            msg_calllistlen = len (msg_callsignlist)
        else:
            msg_calllistlen = 10

        for i in range(0,msg_calllistlen):
            sql = """insert into msg_callsigns (callsign)
            values("""
            sql = sql + "'" + msg_callsignlist[i].upper().strip() + "');"

            run_sql(conn,sql)

    if send_status_types == 1 or send_status_types == 3:
        msg = """

    Since you indicated you are using a Weather Station and would like to have that data sent to Social Media,
    we need to know the callsign(s) of the weatehr station(s) to pull the data.

    Please enter the list below of callsigns in the following format, seperated by commas:

    callsign or callsign-ssid (Ex: AA0ABC, AA0ABC-1, AA0ABC-2 etc)

    Note that there is a max of 20 callsigns that can be entered. Any more than 20 will be cut off.

    """

        print(msg)

        wx_callsignlist = list(map(str,input("Callsign List: ").split(',')))
        if len(wx_callsignlist) < 20:
            wx_calllistlen = len (wx_callsignlist)
        else:
            wx_calllistlen = 20

        for i in range(0,msg_calllistlen):
            sql = """insert into wx_callsigns (callsign)
            values("""
            sql = sql + "'" + wx_callsignlist[i].upper().strip() + "');"

            run_sql(conn,sql)
    

    print(linefeed)    
    aprsfikey = input("Now, please copy and paste your APRS.FI API key here: ")
    if include_wx == 1:
        openweathermapkey = input("Finally, please copy and paste your OpenWeatherMap API Key here: ")

    sql = "update apikeys set aprsfikey = '" + aprsfikey + "', "
    sql = "openweathermapkey = '" + openweathermapkey + "';"
    run_sql(conn,sql) 

    #-----------------------------------------
    clear_screen()

    msg = title_line +"""

    Your database file has been built. 

    If you need to update the database in the future to change configs, just run the an_util.py script with python3 an_util.py and you will be able to update your database. 

    You are now ready to test APRSNotify by typing python3 aprsnotify.py when you are returned to the command prompt.

    Thanks again for using APRSNotify.
    """

    print(msg)

    pause = input("Please press enter when you are ready.")