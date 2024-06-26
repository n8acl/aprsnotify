# Import Libraries
from flask import Flask, render_template, request, Markup
import sqlite3 as sql
import os
from os import system, name

# define Variables
app = Flask(__name__)

database = os.path.dirname(os.path.abspath(__file__)) +  "/aprsnotify.db"
linefeed = "\n"
html_linefeed = "<br>"
current_version = '02032023'
wiki_url = 'https://n8acl.github.io/aprsnotify/'

# Define functions

def create_connection(db_file):
   conn = None
   conn = sql.connect(database)
   conn.row_factory = sql.Row  
   return conn 

def select_sql(conn, sql):
    # Executes SQL for Selects - Returns a "value"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes - Doesn't return anything
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def new(conn, version):

   create_config_table = """ create table if not exists config (
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

   create_aprsstamps_table = """ create table if not exists aprsstamps (
   lastpostime int,
   lastmsgid int,
   lastwxtime int
); """

   create_callsignlist_table = """ create table if not exists callsignlists (
   callsign text null,
   listtype text null
); """

   create_apikeys_table = """ create table if not exists apikeys (
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

   exec_sql(conn, create_config_table)
   exec_sql(conn, create_aprsstamps_table)
   exec_sql(conn, create_callsignlist_table)
   exec_sql(conn, create_apikeys_table)

   sql = """insert into config (
      telegram,
      mastodon,
      discord,
      mattermost,
      units_to_use,
      include_map_image_telegram,
      include_wx,
      send_position_data,
      send_weather_data,
      aprsmsg_notify_telegram,
      aprsmsg_notify_discord,
      aprsmsg_notify_pushover,
      aprsmsg_notify_slack,
      aprsmsg_notify_mattermost,
      club_telegram,
      club_discord,
      club_mattermost,
      club_slack, 
      version)
    values (False,False,False,1,False,False,False,False,False,False,False,False,False,False,False,False,False,'""" + version + """');"""

   exec_sql(conn,sql)

   sql = """insert into apikeys (
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
   )
   values(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null);"""

   exec_sql(conn,sql)

   sql = """insert into aprsstamps (lastpostime, lastmsgid, lastwxtime)
   values(1,1,1);
   """ 
   exec_sql(conn,sql)

   return

# Check to see if the database exists and if not create it. This check for first time run.

if not os.path.exists(database):
   conn = create_connection(database)
   new(conn, current_version)

# Get Version Number from Database
conn = create_connection(database)
ver = select_sql(conn, "select version from config;")
for row in ver:
   version = row[0]
conn.close()

#Set Standard Page Title
page_title = "APRSNotify Configuration Utility <br> Release " + str(version)
page_title = Markup(page_title)

# Define URL routes for Flask

@app.route('/')
def index():
   return render_template('index.html', page_title = page_title)

@app.route('/smkeys')
def smkeys():
   conn = create_connection(database)
   telegram_keys = select_sql(conn, "select ifnull(telegram_bot_token,'None') as telegram_bot_token, ifnull(telegram_poswx_chat_id,'None') as telegram_poswx_chat_id from apikeys")
   mastodon_keys = select_sql(conn, "select ifnull(mastodon_client_id,'None') as mastodon_client_id, ifnull(mastodon_client_secret,'None') as mastodon_client_secret, ifnull(mastodon_api_base_url,'None') as mastodon_api_base_url, ifnull(mastodon_user_access_token,'None') as mastodon_user_access_token from apikeys")
   discord_keys = select_sql(conn, "select ifnull(discord_poswx_wh_url, 'None') as discord_poswx_wh_url from apikeys")
   mattermost_keys = select_sql(conn, "select ifnull(mattermost_poswx_wh_url, 'None') as mattermost_poswx_wh_url, ifnull(mattermost_poswx_api_key, 'None') as mattermost_poswx_api_key from apikeys")
   slack_keys = select_sql(conn, "select ifnull(slack_poswx_wh_url, 'None') as slack_poswx_wh_url from apikeys")
   config_settings = select_sql(conn, "select telegram, mastodon, include_map_image_telegram, discord, mattermost, slack from config")
   return render_template('smkeys.html', config_settings = config_settings, telegram_keys = telegram_keys, mastodon_keys = mastodon_keys, discord_keys = discord_keys, mattermost_keys = mattermost_keys, slack_keys = slack_keys, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/msgsettings')
def msgsettings():
   conn = create_connection(database)
   telegram_keys = select_sql(conn, "select ifnull(telegram_bot_token,'None') as telegram_bot_token, ifnull(ifnull(telegram_aprsmsg_chat_id,telegram_poswx_chat_id),'None') as telegram_aprsmsg_chat_id from apikeys")
   discord_keys = select_sql(conn, "select ifnull(ifnull(discord_aprsmsg_wh_url, discord_poswx_wh_url),'None') as discord_aprsmsg_wh_url from apikeys")
   pushover_keys = select_sql(conn, "select ifnull(pushover_token, 'None') as pushover_token, ifnull(pushover_userkey, 'None') as pushover_userkey from apikeys")
   mattermost_keys = select_sql(conn, "select ifnull(ifnull(mattermost_aprsmsg_wh_url, mattermost_poswx_wh_url),'None') as mattermost_aprsmsg_wh_url, ifnull(ifnull(mattermost_aprsmsg_api_key, mattermost_poswx_api_key),'None') as mattermost_aprsmsg_api_key from apikeys")
   slack_keys = select_sql(conn, "select ifnull(ifnull(slack_aprsmsg_wh_url, slack_poswx_wh_url),'None') as slack_aprsmsg_wh_url from apikeys")
   config_settings = select_sql(conn, "select aprsmsg_notify_telegram, aprsmsg_notify_discord, aprsmsg_notify_pushover, aprsmsg_notify_mattermost, aprsmsg_notify_slack from config")
   
   return render_template('msgsettings.html', config_settings = config_settings, telegram_keys = telegram_keys, discord_keys = discord_keys, pushover_keys = pushover_keys, mattermost_keys = mattermost_keys, slack_keys = slack_keys, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/clubsettings')
def clubsettings():
   conn = create_connection(database)
   telegram_keys = select_sql(conn, "select ifnull(ifnull(telegram_bot_token,telegram_club_bot_token),'None') as telegram_club_bot_token, ifnull(telegram_club_chat_id,'None') as telegram_club_chat_id from apikeys")
   discord_keys = select_sql(conn, "select ifnull(discord_club_wh_url, 'None') as discord_club_wh_url from apikeys")
   mattermost_keys = select_sql(conn, "select ifnull(mattermost_club_wh_url,'None') as mattermost_club_wh_url, ifnull(mattermost_club_api_key,'None') as mattermost_club_api_key from apikeys")
   slack_keys = select_sql(conn, "select ifnull(slack_club_wh_url,'None') as slack_club_wh_url from apikeys")
   config_settings = select_sql(conn, "select club_telegram, club_discord, club_mattermost, club_slack from config")

   return render_template('clubsettings.html', config_settings = config_settings, telegram_keys = telegram_keys, discord_keys = discord_keys, mattermost_keys = mattermost_keys, slack_keys = slack_keys, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/otherapikeys')
def otherapikeys():
   conn = create_connection(database)
   apikeys = select_sql(conn, "select aprsfikey, openweathermapkey from apikeys")
   return render_template('otherapikeys.html', apikeys = apikeys, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/configuration')
def configuration():
   conn = create_connection(database)
   configsettings = select_sql(conn, "select units_to_use, include_wx, send_position_data, send_weather_data from config")
   return render_template('configuration.html', configs = configsettings, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/callsignlists')
def callsignlists():
   conn = create_connection(database)
   poscallsignlist = select_sql(conn, "select ifnull(callsign,'None') as poscallsignlist from callsignlists where listtype = 'POS'")
   wxcallsignlist = select_sql(conn, "select ifnull(callsign,'None') as wxcallsignlist from callsignlists where listtype = 'WX'")
   msgcallsignlist = select_sql(conn, "select ifnull(callsign,'None') as msgcallsignlist from callsignlists where listtype = 'MSG'")      
   poscnt = select_sql(conn, "select count(callsign) as poscnt from callsignlists where listtype = 'POS'")
   wxcnt = select_sql(conn, "select count(callsign) as wxcnt from callsignlists where listtype = 'WX'")
   msgcnt = select_sql(conn, "select count(callsign) as msgcnt from callsignlists where listtype = 'MSG'") 

   return render_template('callsignlists.html', poscallsignlist = poscallsignlist, wxcallsignlist = wxcallsignlist, msgcallsignlist = msgcallsignlist, poscnt = poscnt, wxcnt = wxcnt, msgcnt = msgcnt, page_title = page_title, wiki_url = wiki_url)
   conn.close()

@app.route('/update_api_keys', methods = ['POST', 'GET'])
def update_api_keys():
   conn = create_connection(database)

   if request.method == 'POST' and request.form["app"] == "telegram":

      header = "-------------------  " + request.form["app"].capitalize() + " API Keys -------------------"

      try:
         telegram_bot_token = request.form["telegram_bot_token"]
         telegram_poswx_chat_id = request.form["telegram_poswx_chat_id"]


         sql = "update apikeys set "
         sql = sql + "telegram_bot_token = '" + request.form["telegram_bot_token"] + "', "
         sql = sql + "telegram_poswx_chat_id = '" + request.form["telegram_poswx_chat_id"] + "';"

         exec_sql(conn,sql)

         sql = "update config set telegram = "

         if request.form["send_to_telegram"] == '1':
            sql = sql + "True, "
         else:
            sql = sql + "False, "

         sql = sql + "include_map_image_telegram = "
         
         if request.form["include_map_image_telegram"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"

         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mastodon":

      header = "-------------------  " + request.form["app"].capitalize() + " API Keys -------------------"

      try:

         mastodon_instance_url = request.form["mastodon_instance_url"]
         mastodon_bot_app_name = request.form["mastodon_bot_app_name"]
         mastodon_username = request.form["mastodon_username"]
         mastodon_password = request.form["mastodon_password"]

         client_keys = Mastodon.create_app(request.form["mastodon_bot_app_name"], scopes=['read', 'write'], api_base_url=request.form["mastodon_instance_url"])

         mastodon_api = Mastodon(client_keys[0], client_keys[1], api_base_url = request.form["mastodon_instance_url"])

         access_token = mastodon_api.log_in(request.form["mastodon_username"], request.form["mastodon_password"], scopes=["read", "write"])

         sql = "update apikeys set "
         sql = sql + "mastodon_client_id = '" + client_keys[0] + "', "
         sql = sql + "mastodon_client_secret = '" + client_keys[1] + "', "
         sql = sql + "mastodon_api_base_url = '" + request.form["mastodon_instance_url"] + "', "
         sql = sql + "mastodon_user_access_token = '" + access_token + "';"

         exec_sql(conn,sql)

         sql = "update config set mastodon = " 
         
         if request.form["send_to_mastodon"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "discord":

      header = "-------------------  " + request.form["app"].capitalize() + " Webhook -------------------"

      try:

         discord_webhook_url = request.form["discord_webhook_url"]

         sql = "update apikeys set "
         sql = sql + "discord_poswx_wh_url = '" + request.form["discord_poswx_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set discord = " 
         if request.form["send_to_discord"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  

         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mattermost":

      header = "-------------------  " + request.form["app"].capitalize() + " Webhook -------------------"

      try:

         mattermost_poswx_wh_url = request.form["mattermost_poswx_wh_url"]
         mattermost_poswx_api_key = request.form["mattermost_poswx_api_key"]

         sql = "update apikeys set "
         sql = sql + "mattermost_poswx_wh_url = '" + request.form["mattermost_poswx_wh_url"] + "', "
         sql = sql + "mattermost_poswx_api_key = '" + request.form["mattermost_poswx_api_key"] + "';"

         exec_sql(conn,sql)

         sql = "update config set mattermost = " 
         
         if request.form["send_to_mattermost"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "slack":

      header = "-------------------  " + request.form["app"].capitalize() + " Webhook -------------------"

      try:

         slack_poswx_wh_url = request.form["slack_poswx_wh_url"]

         sql = "update apikeys set "
         sql = sql + "slack_poswx_wh_url = '" + request.form["slack_poswx_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set slack = " 
         
         if request.form["send_to_slack"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()
 
   if request.method == 'POST' and request.form["app"] == "aprsfi":

      header = "-------------------  " + request.form["app"].capitalize() + " API Key -------------------"

      try:

         aprsfikey = request.form["aprsfikey"]

         sql = "update apikeys set "
         sql = sql + "aprsfikey = '" + aprsfikey + "';"

         exec_sql(conn,sql)

         msg = request.form["app"].capitalize() + " API Key updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="otherapikeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "openweathermap":

      header = "-------------------  " + request.form["app"].capitalize() + " API Key -------------------"

      try:

         openweathermapkey = request.form["openweathermapkey"]

         sql = "update apikeys set "
         sql = sql + "openweathermapkey = '" + openweathermapkey + "';"

         exec_sql(conn,sql)

         msg = request.form["app"].capitalize() + " API Key updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="otherapikeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

@app.route('/update_configs', methods = ['POST', 'GET'])
def update_configs():
   conn = create_connection(database)

   header = "-------------------  Configs Updated -------------------"

   try:

      sql = "update config set "
      sql = sql + "units_to_use = " + request.form["units_to_use"] + ", "
      sql = sql + "include_wx = " 
      
      if request.form["include_wx"] == '1':
         sql = sql + "True, "
      else:
         sql = sql + "False, " 
            
      sql = sql + "send_position_data = " 
      
      if request.form["send_position_data"] == '1':
         sql = sql + "True, "
      else:
         sql = sql + "False, " 
      
      sql = sql + "send_weather_data = " 
      
      if request.form["send_weather_data"] == '1':
         sql = sql + "True;"
      else:
         sql = sql + "False;" 

      exec_sql(conn,sql)

      msg = "Configurations settings updated."
   except:
      conn.rollback()
      msg = "Error in Operation."
   finally:
      return render_template("results.html", msg = msg, header = header, page="configuration", page_title = page_title, wiki_url = wiki_url)
      conn.close()

@app.route('/update_msg_settings', methods = ['POST', 'GET'])
def update_msg_settings():
   conn = create_connection(database)

   if request.method == 'POST' and request.form["app"] == "pushover":

      header = "-------------------  " + request.form["app"].capitalize() + " Message Notification Settings -------------------"

      try:
         pushover_token = request.form["pushover_token"]
         pushover_userkey = request.form["pushover_userkey"]
         aprsmsg_notify_pushover = request.form["aprsmsg_notify_pushover"]

         sql = "update apikeys set "
         sql = sql + "pushover_token = '" + request.form["pushover_token"] + "', "
         sql = sql + "pushover_userkey = '" + request.form["pushover_userkey"] + "';"

         exec_sql(conn,sql)

         sql = "update config set aprsmsg_notify_pushover = "
         if request.form["aprsmsg_notify_pushover"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;" 


         exec_sql(conn,sql)        

         msg = request.form["app"].capitalize() + " Message Notification Settings updated."

      except:
         conn.rollback()
         msg = "Error in Operation."

      finally:
         return render_template("results.html", msg = msg, header = header, page="msgkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "discord":

      header = "-------------------  " + request.form["app"].capitalize() + " Message Notification Settings -------------------"

      try:

         discord_aprsmsg_wh_url = request.form["discord_aprsmsg_wh_url"]

         sql = "update apikeys set "
         sql = sql + "discord_aprsmsg_wh_url = '" + request.form["discord_aprsmsg_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set aprsmsg_notify_discord = "

         if request.form["aprsmsg_notify_discord"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"      
         
         exec_sql(conn,sql) 

         msg = request.form["app"].capitalize() + " Message Notification Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="msgkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "telegram":

      header = "-------------------  " + request.form["app"].capitalize() + " Message Notification Settings -------------------"

      try:
         telegram_bot_token = request.form["telegram_bot_token"]
         telegram_aprsmsg_chat_id = request.form["telegram_aprsmsg_chat_id"]


         sql = "update apikeys set "
         sql = sql + "telegram_bot_token = '" + request.form["telegram_bot_token"] + "', "
         sql = sql + "telegram_aprsmsg_chat_id = '" + request.form["telegram_aprsmsg_chat_id"] + "';"

         exec_sql(conn,sql)

         sql = "update config set aprsmsg_notify_telegram = "

         if request.form["aprsmsg_notify_telegram"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;" 

         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Message Notification Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="msgkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mattermost":

      header = "-------------------  " + request.form["app"].capitalize() + " Message Notification Webhook -------------------"

      try:

         mattermost_aprsmsg_wh_url = request.form["mattermost_aprsmsg_wh_url"]
         mattermost_aprsmsg_api_key = request.form["mattermost_aprsmsg_api_key"]

         sql = "update apikeys set "
         sql = sql + "mattermost_aprsmsg_wh_url = '" + request.form["mattermost_aprsmsg_wh_url"] + "', "
         sql = sql + "mattermost_aprsmsg_api_key = '" + request.form["mattermost_aprsmsg_api_key"] + "';"

         exec_sql(conn,sql)

         sql = "update config set aprsmsg_notify_telegram = " 
         
         if request.form["aprsmsg_notify_mattermost"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Message Notification Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="msgkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "slack":

      header = "-------------------  " + request.form["app"].capitalize() + " Messaging Webhook -------------------"

      try:

         slack_aprsmsg_wh_url = request.form["slack_aprsmsg_wh_url"]

         sql = "update apikeys set "
         sql = sql + "slack_aprsmsg_wh_url = '" + request.form["slack_aprsmsg_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set aprsmsg_notify_slack = " 
         
         if request.form["aprsmsg_notify_slack"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Message Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="msgkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

@app.route('/update_club_settings', methods = ['POST', 'GET'])
def update_club_settings():
   conn = create_connection(database)

   if request.method == 'POST' and request.form["app"] == "discord":

      header = "-------------------  " + request.form["app"].capitalize() + " Club Settings -------------------"

      try:

         discord_club_wh_url = request.form["discord_club_wh_url"]

         sql = "update apikeys set "
         sql = sql + "discord_club_wh_url = '" + request.form["discord_club_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set club_discord = "

         if request.form["club_discord"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"      
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Club Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="clubkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "telegram":

      header = "-------------------  " + request.form["app"].capitalize() + " Club Settings -------------------"

      try:
         telegram_club_bot_token = request.form["telegram_club_bot_token"]
         telegram_club_chat_id = request.form["telegram_club_chat_id"]


         sql = "update apikeys set "
         sql = sql + "telegram_club_bot_token = '" + request.form["telegram_club_bot_token"] + "', "
         sql = sql + "telegram_club_chat_id = '" + request.form["telegram_club_chat_id"] + "';"

         exec_sql(conn,sql)

         sql = "update config set club_telegram = "

         if request.form["club_telegram"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;" 

         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Club Notification Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="clubkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mattermost":

      header = "-------------------  " + request.form["app"].capitalize() + " Club Notification Webhook -------------------"

      try:

         mattermost_club_wh_url = request.form["mattermost_club_wh_url"]
         mattermost_club_api_key = request.form["mattermost_club_api_key"]

         sql = "update apikeys set "
         sql = sql + "mattermost_club_wh_url = '" + request.form["mattermost_club_wh_url"] + "', "
         sql = sql + "mattermost_club_api_key = '" + request.form["mattermost_club_api_key"] + "';"

         exec_sql(conn,sql)

         sql = "update config set club_mattermost = " 
         
         if request.form["club_mattermost"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Club Notification Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="clubkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "slack":

      header = "-------------------  " + request.form["app"].capitalize() + " Messaging Webhook -------------------"

      try:

         slack_club_wh_url = request.form["slack_club_wh_url"]

         sql = "update apikeys set "
         sql = sql + "slack_club_wh_url = '" + request.form["slack_club_wh_url"] + "';"

         exec_sql(conn,sql)

         sql = "update config set club_slack = " 
         
         if request.form["club_slack"] == '1':
            sql = sql + "True;"
         else:
            sql = sql + "False;"  
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Club Settings updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="clubkeys", page_title = page_title, wiki_url = wiki_url)
         conn.close()

@app.route('/update_callsign_lists', methods = ['POST', 'GET'])
def update_callsign_lists():
   conn = create_connection(database)

   header = "-------------------  " + request.form["listtype"].upper() + " Callsign List -------------------"

   try:
      callsignlist = request.form["callsignlist"].split(",")
      listtype = request.form["listtype"] # POS, WX, Msg
      function = request.form["function"] # 1 = Add, 0 = delete


      sql = "select count(callsign) as callcnt from callsignlists where listtype = '" + listtype + "';"
      callcnt = select_sql(conn, sql)
      for row in callcnt:
         callcount = row[0]

      if function == '1':
         if listtype == 'POS' and callcount >= 20:
            msg = "Error: You cannot add more Callsigns to the POS list. You have reached the Max Allowed."
         elif listtype == 'MSG' and callcount >= 10:
            msg = "Error: You cannot add more Callsigns to the MSG list. You have reached the Max Allowed."
         else:
            for x in range(0,len(callsignlist)):
               sql = "insert into callsignlists (callsign, listtype) values ('" + (callsignlist[x].strip()).upper() + "','" + listtype.upper() + "');"
               exec_sql(conn,sql)
            msg = "Callsign(s) inserted into " + request.form["listtype"].upper() + " Callsign List."
      else:
         for x in range(0,len(callsignlist)):
            sql = "Delete from callsignlists where callsign = '" + (callsignlist[x].strip()).upper() + "' and listtype = '" + listtype + "';"
            exec_sql(conn,sql)
         msg = "Callsign(s) " + request.form["callsignlist"] + " deleted from " + request.form["listtype"].upper() + " Callsign List."

   except:
      conn.rollback()
      msg = "Error in Operation."

   finally:
      return render_template("results.html", msg = msg, header = header, page="callsignlists", page_title = page_title, wiki_url = wiki_url)
      conn.close()


# Main Driver

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5001, debug=True)