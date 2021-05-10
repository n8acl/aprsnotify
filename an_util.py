# Import Libraries

import sqlite3
import os
import sys
from os import system, name
from sqlite3 import Error
from mastodon import Mastodon

# Define Variables
database = os.path.dirname(os.path.abspath(__file__)) +  "/aprsnotify.db"
setup = os.path.dirname(os.path.abspath(__file__)) +  "/new.py"
linefeed = "\n"
selection = 0
header = """
################################################
# APRSNotify Configuration Utility
################################################

"""

# Define Functions
def clear_screen(): # Defines function to clear the screen to make output easier to read
    if name == 'nt': # windows
        _ = system('cls')
    else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
        _ = system('clear')

def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes - Doesn't return anything
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def select_sql(conn,sql):
    # Executes SQL for Selects - Returns a "value"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def create_connection(db_file):
    # Creates connection to APRSNotify.db SQLlite3 Database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

######################################################################################################################
# Check to see if the database file exists and if not, run the initial setup. Otherwise, carry on

if not os.path.exists(database):
    import new
    conn = create_connection(database)
    new.setup(conn)
    sys.exit()

######################################################################################################################
# Load Data from Database into variables

# Create Database Connection
conn = create_connection(database)

# Get Main Menu items from database

sql = """select 
    menu_id, menu_item 
    from anutilmenu where submenu_id = 1 and menu_id <> 0"""

main_menu = select_sql(conn, sql)

##########################################
# Define operational Functions

def update_apikeys(keyid,keyname,old_key):

    if keyid != '':
        apikey_name = keyid + "_" + keyname.replace(" ","_").lower()
    else:
        apikey_name = keyname.replace(" ","_").lower()

    print("Update " + keyname)
    print("---------------------------")
    print("Current " + keyname + ": " + old_key)
    new_key=input("Paste new " + keyname + " here: ")

    sql = "Update apikeys set " + apikey_name + " = '" + new_key + "';"

    exec_sql(conn,sql)

def update_callsignlists(listtype,func):
    
    callsignlist = []
    
    sql = "select callsign from " + listtype.lower() + "_callsigns;"
    
    result = select_sql(conn, sql)

    for row in result:
        callsignlist.append(row[0])
    
    print(linefeed)
    print("Current " + listtype.upper() + " Callsign List")
    print("---------------------------")
    print(",".join(callsignlist))
    print(linefeed)
 
    if func == 1:
        modify_callsign = input("Please Enter the callsign to Add: ")
        sql = "insert into " + listtype.lower() +"_callsigns (callsign) values('" + modify_callsign.upper() + "');"
    else:
        modify_callsign = input("Please Enter the callsign to Delete: ")
        sql = "delete from " + listtype.lower() +"_callsigns where callsign = '" + modify_callsign.upper() + "';"

    exec_sql(conn,sql)

def update_config(key,value):
    sql = "update config set " + key + " = " + str(value) +";"

    exec_sql(conn,sql)

##########################################
# Define Menu Functions

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

    exec_sql(conn, sql)
    
def set_telgram_keys(conn):
    msg = "In order to use Telegram, You will need to obtain 2 Keys from them: The Bot Token and Your Chat ID " + linefeed + linefeed
    print(msg)
    my_bot_token = input("Please copy and paste your Bot Token here: ")
    my_chat_id = input("Please copy and paste your Chatid here: ")
    print(linefeed)

    sql = "update apikeys set telegram_bot_token = '" + my_bot_token +"', "
    sql = sql + "telegram_my_chat_id = '" + my_chat_id + "';"

    exec_sql(conn, sql)

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
    
    exec_sql(conn,sql)

def fn_twitterapi_menu():
    while True:
        sql = """select 
        menu_id, menu_item 
        from anutilmenu where submenu_id = 6"""

        menu = select_sql(conn, sql)

        sql = """select 
        twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret
        from apikeys"""

        keys = select_sql(conn, sql)

        selection = 0 

        clear_screen()
        print(header)
        print("Twitter API Keys Configuration Menu")
        print("---------------------------")
        print(linefeed)
        print("Current Keys")
        print("---------------------------")
        print("Consumer Key: " + keys[0][0])
        print("Consumer Secret: " + keys[0][1])
        print("Access Token: " + keys[0][2])            
        print("Access Secret: " + keys[0][3])
        print(linefeed)

        for row in menu:
            entry = str(row[0]) + ": " + row[1] 
            print(entry)

        selection = int(input("Please Enter Selection: "))
        print(linefeed)

        if selection == 1:
            update_apikeys("twitter","Consumer Key",keys[0][0])
        if selection == 2:
           update_apikeys("twitter","Consumer Secret",keys[0][1])
        if selection == 3:
            update_apikeys("twitter","Access Token",keys[0][2])
        if selection == 4:
            update_apikeys("twitter","Access Secret",keys[0][3])
        if selection == 5:
            return        
        pause=input("Press Enter to Continue")

def fn_telegramapi_menu():
    while True:
        sql = """select 
            menu_id, menu_item 
            from anutilmenu where submenu_id = 7"""

        menu = select_sql(conn, sql)

        sql = """select 
        telegram_bot_token, telegram_my_chat_id
        from apikeys"""

        keys = select_sql(conn, sql)

        selection = 0 

        clear_screen()
        print(header)
        print("Telegram API Keys Configuration Menu")
        print("---------------------------")
        print(linefeed)
        print("Current Keys")
        print("---------------------------")
        print("Bot Token: " + keys[0][0])
        print("My Chat ID: " + keys[0][1])
        print(linefeed)

        for row in menu:
            entry = str(row[0]) + ": " + row[1] 
            print(entry)

        selection = int(input("Please Enter Selection: "))
        print(linefeed)

        if selection == 1:
            update_apikeys("telegram","Bot Token",keys[0][0])
        if selection == 2:
            update_apikeys("telegram","My Chat ID",keys[0][1])
        if selection == 3:
            return        
        pause=input("Press Enter to Continue")

def fn_mastodonapi_menu():
    while True:
        sql = """select 
            menu_id, menu_item 
            from anutilmenu where submenu_id = 8"""

        menu = select_sql(conn, sql)

        sql = """select 
        mastodon_client_id, mastodon_client_secret, mastodon_api_base_url, mastodon_user_access_token
        from apikeys"""

        keys = select_sql(conn, sql)

        selection = 0 

        clear_screen()
        print(header)
        print("Mastodon API Keys Configuration Menu")
        print("---------------------------")
        print(linefeed)
        print("Current Keys")
        print("---------------------------")
        print("Client ID: " + keys[0][0])
        print("Client Secret: " + keys[0][1])
        print("API Base URL: " + keys[0][2])            
        print("User Access Token: " + keys[0][3])
        print(linefeed)

        for row in menu:
            entry = str(row[0]) + ": " + row[1] 
            print(entry)

        selection = int(input("Please Enter Selection: "))
        print(linefeed)

        if selection == 1:
            print("Obtain New Keys")
            print("---------------------------")
            mastodon_instance_url = input("First, I need the url of the instance your bot account is on (EX: https://botsin.space): ")
            mastodon_bot_app_name = input("Now I need to know what you want to call the app. Make it unique (EX: my_aprs_bot): ")
            mastodon_username = input("Now I need the username and password for the bot account: ")
            mastodon_password = input("Finally I need the password for the bot account: ")

            client_keys = Mastodon.create_app(mastodon_bot_app_name, scopes=['read', 'write'], api_base_url=mastodon_instance_url)

            mastodon_api = Mastodon(client_keys[0], client_keys[1], api_base_url = mastodon_instance_url)

            access_token = mastodon_api.log_in(mastodon_username, mastodon_password, scopes=["read", "write"])

            sql = "update apikeys set mastodon_client_id = '" + client_keys[0] + "', "
            sql = sql + "mastodon_client_secret = '" + client_keys[1] + "', "
            sql = sql + "mastodon_api_base_url = '" + mastodon_instance_url + "', "
            sql = sql + "mastodon_user_access_token = '" + access_token + "';"
            exec_sql(conn,sql)
        if selection == 2:
            return        
        pause=input("Press Enter to Continue")

def fn_smapikeys_menu():

    while True:
        sql = """select 
            menu_id, menu_item 
            from anutilmenu where submenu_id = 3"""

        menu = select_sql(conn, sql)

        selection = 0 

        clear_screen()
        print(header)
        print("Social Media API Keys Configuration Menu")
        print("---------------------------")

        for row in menu:
            entry = str(row[0]) + ": " + row[1]
            print(entry)  

        selection = int(input("Please Enter Selection: "))

        if selection == 1:
            fn_twitterapi_menu()
        if selection == 2:
            fn_telegramapi_menu()
        if selection == 3:
            fn_mastodonapi_menu()
        if selection == 4:
            return

def fn_callsignmodify_menu():

    while True:
        pos_callsign_list=[]
        msg_callsign_list=[]
        wx_callsign_list=[]

        sql = """select 
            menu_id, menu_item 
            from anutilmenu where submenu_id = 9"""

        menu = select_sql(conn, sql)

        sql = "select callsign from pos_callsigns;"

        results = select_sql(conn,sql)

        for row in results:
            pos_callsign_list.append(row[0])

        sql = "select callsign from msg_callsigns;"

        results = select_sql(conn,sql)

        for row in results:
            msg_callsign_list.append(row[0])

        sql = "select callsign from wx_callsigns;"

        results = select_sql(conn,sql)

        for row in results:
            wx_callsign_list.append(row[0])

        selection = 0 

        clear_screen()
        print(header)
        print("POS/MSG Callsign List Configuration Menu")
        print("---------------------------")
        print("POS = Position Tracking")
        print("MSG = Message Tracking")
        print("WX = Weather Station Tracking")
        print(linefeed)
        print("POS Callsigns: " + ", ".join(pos_callsign_list))
        print("MSG Callsigns: " + ", ".join(msg_callsign_list))
        print("WX Callsigns: " + ", ".join(wx_callsign_list))
        print(linefeed)

        for row in menu:
            entry = str(row[0]) + ": " + row[1]
            print(entry)  

        selection = int(input("Please Enter Selection: "))

        if selection == 1:
            update_callsignlists('pos',1)
        if selection == 2:
            update_callsignlists('pos',2)
        if selection == 3:
            update_callsignlists('msg',1)
        if selection == 4:
            update_callsignlists('msg',2)
        if selection == 5:
            update_callsignlists('wx',1)
        if selection == 6:
            update_callsignlists('wx',2)
        return

def fn_apikeys_menu():
    while True:
        sql = """select 
        menu_id, menu_item 
        from anutilmenu where submenu_id = 11"""

        menu = select_sql(conn, sql)

        sql = """select
        aprsfikey, openweathermapkey
        from apikeys"""

        keys = select_sql(conn,sql)

        selection = 0 

        clear_screen()
        print(header)
        print("API Keys Configuration Menu")
        print("---------------------------")
        print(linefeed)
        print("Current Keys")
        print("---------------------------")
        print("APRSFI API Key: " + keys[0][0])
        print("OpenWeatherMap API Key: " + keys[0][1])
        print(linefeed)


        for row in menu:
            entry = str(row[0]) + ": " + row[1] 
            print(entry)

        selection = int(input("Please Enter Selection: "))
        print(linefeed)

        if selection == 1:
            update_apikeys("","aprsfikey",keys[0][0])
        if selection == 2:
            update_apikeys("","openweathermapkey",keys[0][1])
        if selection == 3:
           return        
        pause=input("Press Enter to Continue")

def fn_configuration_menu():
    while True:
        sql = """select 
        send_to_all,
        send_to_twitter,
        send_to_telegram,
        send_to_mastodon,
        units_to_use,
        enable_aprs_msg_notify,
        include_map_image,
        include_wx,
        send_position_data,
        send_weather_data
        from config"""

        configs = select_sql(conn,sql)

        sql = """select 
        menu_id, menu_item, current_state
        from vw_config_menu
        """

        if configs[0][0] == 1:
            sql = sql + "where menu_id not in (2,3,4)"

        menu = select_sql(conn, sql)

        sql = """select 
        max(menu_id) as maxmenuid
        from vw_config_menu
        """

        if configs[0][0] == 1:
            sql = sql + "where menu_id not in (2,3,4)"

        maxmenuid = select_sql(conn, sql)

        selection = 0 

        clear_screen()
        print(header)
        print("APRSNotify Configuration Menu")
        print("---------------------------")

        x = 0
        for row in menu:
            if row[0] != maxmenuid[0][0]:
                entry = str(row[0]) + ": " + row[1] + " | Currently: " + row[2]
            else:
                entry = str(row[0]) + ": " + row[1]

            print(entry)  

        selection = int(input("Please Enter Selection: "))
        
        if selection != maxmenuid[0][0]:
            config_toggle(selection,configs)
        else:
            return

def config_toggle(selection, configs):

    sql = """select 
    ifnull(twitter_consumer_key,'None') as twitter_consumer_key,
    ifnull(twitter_consumer_secret,'None') as twitter_consumer_secret,
    ifnull(twitter_access_token,'None') as twitter_access_token,
    ifnull(twitter_access_secret,'None') as twitter_access_secret,
    ifnull(telegram_bot_token,'None') as telegram_bot_token,
    ifnull(telegram_my_chat_id,'None') as telegram_my_chat_id,
    aprsfikey,
    ifnull(openweathermapkey,'None') as openweathermapkey,
    ifnull(mastodon_client_id,'None') as mastodon_client_id,
    ifnull(mastodon_client_secret,'None') as mastodon_client_secret,
    ifnull(mastodon_api_base_url,'None') as mastodon_api_base_url,
    ifnull(mastodon_user_access_token,'None') as mastodon_user_access_token
    from apikeys"""

    apikeys = select_sql(conn,sql)

    if selection == 1:
        if configs[0][0] == 0:
            sql = "update config set send_to_all = 1, send_to_twitter = 0, send_to_telegram = 0, send_to_mastodon = 0"
            exec_sql(conn,sql)
            print(linefeed)
            print("Since you are turning on Send to All, we need to check to make sure you have your API keys set.")
            if apikeys[0][0] == 'None':
                print(linefeed)
                set_twitter_keys(conn)
            if apikeys[0][4] == 'None':
                print(linefeed)
                set_telegram_keys(conn)
            if apikeys[0][8] == 'None':
                print(linefeed)
                set_mastodon_keys(conn)
        else:
            sql = "update config set send_to_all = 0"
            exec_sql(conn,sql)
            print(linefeed)
            print("Since you are turning off Send to All, You need to have one Service Active.")
            while True and selection not in [1,2,3]:
                msg = """
                1: Twitter
                2: Telegram
                3: Mastodon
                """           
                selection = input("Please choose a service")
            if selection == '1':
                update_config("send_to_twitter",1)
                if apikeys[0][0] == 'None':
                    print(linefeed)
                    set_twitter_keys(conn)
                else:
                    print(linefeed)
                    pause = input("Your Twitter Keys are already set. Press enter to continue.")
            if selection == '2':
                update_config("send_to_telegram",1)
                if apikeys[0][4] == 'None':
                    print(linefeed)
                    set_telegram_keys(conn)
                else:
                    print(linefeed)
                    pause = input("Your Telegram Keys are already set. Press enter to continue.")
            if selection == '3':
                update_config("send_to_mastodon",1)
                if apikeys[0][8] == 'None':
                    print(linefeed)
                    set_mastodon_keys(conn)
                else:
                    print(linefeed)
                    pause = input("Your Mastodon Keys are already set. Press enter to continue.")
    if selection == 2:
        if configs[0][1] == 0:
            update_config("send_to_twitter",1)
            if apikeys[0][0] == 'None':
                print(linefeed)
                set_twitter_keys(conn)
            else:
                print(linefeed)
                pause = input("Your Twitter Keys are already set. Press enter to continue.")
        else:
            update_config("send_to_twitter",0)
    if selection == 3:
        if configs[0][2] == 0:
            update_config("send_to_telegram",1)
            if apikeys[0][4] == 'None':
                print(linefeed)
                set_telegram_keys(conn)
            else:
                print(linefeed)
                pause = input("Your Telegram Keys are already set. Press enter to continue.")
        else:
            update_config("send_to_telegram",0)
    if selection == 4:
        if configs[0][3] == 0:
            update_config("send_to_mastodon",1)
            if apikeys[0][8] == 'None':
                print(linefeed)
                set_mastodon_keys(conn)
            else:
                print(linefeed)
                pause = input("Your Mastodon Keys are already set. Press enter to continue.")
        else:
            update_config("send_to_mastodon",0)
    if selection == 5:
        if configs[0][4] == 1:
            update_config("units_to_use",2)
        else:
            update_config("units_to_use",1)
    if selection == 6:
        if configs[0][5] == 0:
            update_config("enable_aprs_msg_notify",1)
        else:
            update_config("enable_aprs_msg_notify",0)
    if selection == 7:
        if configs[0][6] == 0:
            update_config("include_map_image",1)
        else:
            update_config("include_map_image",0)
    if selection == 8:
        if configs[0][7] == 0:
            update_config("include_wx",1)
        else:
            update_config("include_wx",0)
    if selection == 9:
        if configs[0][8] == 0:
            update_config("send_position_data",1)
        else:
            update_config("send_position_data",0)   
    if selection == 10:
        if configs[0][9] == 0:
            update_config("send_weather_data",1)
        else:
            update_config("send_weather_data",0)
    return

    

##########################################
# Create main menu

while True and selection != 5:
    clear_screen()
    print(header)
    print("Main Menu")
    print("---------------------------")

    for row in main_menu:
        entry = str(row[0]) + ": " + row[1]
        print(entry)  

    selection = int(input("Please Enter Selection: "))
    print(linefeed)

    if selection == 1:
        fn_smapikeys_menu()
    if selection == 2:
        fn_apikeys_menu()
    if selection == 3:
        fn_callsignmodify_menu()
    if selection == 4:
        fn_configuration_menu()

