# Import Libraries
from flask import Flask, render_template, request
import sqlite3 as sql
import os
from os import system, name

# define Variables
app = Flask(__name__)

database = os.path.dirname(os.path.abspath(__file__)) +  "/aprsnotify.db"
version = 5.0
page_title = "APRSNotify " + str(version) + " Configuration Utility"

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
   send_to_twitter int,
   send_to_telegram int,
   send_to_mastodon int,
   units_to_use int,
   enable_aprs_msg_notify int,
   include_map_image int,
   include_wx int,
   send_position_data int,
   send_weather_data int,
   send_to_discord int,
   send_to_mattermost int,
   version float
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
   mastodon_user_access_token text null,
   discord_webhook_url text null,
   mattermost_webhook_url text null
); """

   exec_sql(conn, create_config_table)
   exec_sql(conn, create_aprsstamps_table)
   exec_sql(conn, create_callsignlist_table)
   exec_sql(conn, create_apikeys_table)

   sql = """insert into config (send_to_twitter, send_to_telegram, send_to_mastodon, units_to_use, enable_aprs_msg_notify, 
    include_map_image, include_wx,send_position_data, send_weather_data, send_to_discord, send_to_mattermost, version)
    values (0,0,0,1,0,0,0,0,0,0,0,""" + str(version) + """);"""

   exec_sql(conn,sql)

   sql = """insert into apikeys (twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret,
   telegram_bot_token, telegram_my_chat_id, aprsfikey, openweathermapkey, discord_webhook_url, mattermost_webhook_url)
   values(null,null,null,null,null,null,null,null,null,null);"""

   exec_sql(conn,sql)

   sql = """insert into aprsstamps (lastpostime, lastmsgid, lastwxtime)
   values(1,1,1);
   """ 
   exec_sql(conn,sql)

   return

# Check to see if the database exists and if not create it. This check for first time run.

if not os.path.exists(database):
   conn = create_connection(database)
   new(conn, version)

# Define URL routes for Flask

@app.route('/')
def index():
   return render_template('index.html', page_title = page_title)

@app.route('/smkeys')
def smkeys():
   conn = create_connection(database)
   twitter_keys = select_sql(conn, "select twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret from apikeys")
   telegram_keys = select_sql(conn, "select telegram_bot_token, telegram_my_chat_id from apikeys")
   mastodon_keys = select_sql(conn, "select mastodon_client_id, mastodon_client_secret, mastodon_api_base_url, mastodon_user_access_token from apikeys")
   discord_keys = select_sql(conn, "select ifnull(discord_webhook_url, 'None') as discord_webhook_url from apikeys")
   config_settings = select_sql(conn, "select send_to_twitter, send_to_telegram, send_to_mastodon, enable_aprs_msg_notify, include_map_image, send_to_discord, send_to_mattermost from config")
   return render_template('smkeys.html',twitter_keys = twitter_keys, config_settings = config_settings, telegram_keys = telegram_keys, mastodon_keys = mastodon_keys, discord_keys = discord_keys, page_title = page_title)
   conn.close()

@app.route('/otherapikeys')
def otherapikeys():
   conn = create_connection(database)
   apikeys = select_sql(conn, "select aprsfikey, openweathermapkey from apikeys")
   return render_template('otherapikeys.html', apikeys = apikeys, page_title = page_title)
   conn.close()

@app.route('/configuration')
def configuration():
   conn = create_connection(database)
   configsettings = select_sql(conn, "select units_to_use, include_wx, send_position_data, send_weather_data from config")
   return render_template('configuration.html', configs = configsettings, page_title = page_title)
   conn.close()

@app.route('/callsignlists')
def callsignlists():
   conn = create_connection(database)
   poscallsignlist = select_sql(conn, "select ifnull(callsign,'None') as poscallsignlist from callsignlists where listtype = 'POS'")
   wxcallsignlist = select_sql(conn, "select ifnull(callsign,'None') as wxcallsignlist from callsignlists where listtype = 'WX'")
   msgcallsignlist = select_sql(conn, "select ifnull(callsign,'None') as msgcallsignlist from callsignlists where listtype = 'MSG'")      
  
   return render_template('callsignlists.html', poscallsignlist = poscallsignlist, wxcallsignlist = wxcallsignlist, msgcallsignlist = msgcallsignlist, page_title = page_title)
   conn.close()
   #return render_template('callsignlists.html')


@app.route('/update_api_keys', methods = ['POST', 'GET'])
def update_api_keys():
   conn = create_connection(database)

   if request.method == 'POST' and request.form["app"] == "twitter":

      header = "-------------------  " + request.form["app"].capitalize() + " API Keys -------------------"

      try:
         twitter_consumer_key = request.form["twitter_consumer_key"]
         twitter_consumer_secret = request.form["twitter_consumer_secret"]
         twitter_access_token = request.form["twitter_access_token"]
         twitter_access_secret = request.form["twitter_access_secret"]
         send_to_twitter = request.form["send_to_twitter"]

         sql = "update apikeys set "
         sql = sql + "twitter_consumer_key = '" + twitter_consumer_key + "', "
         sql = sql + "twitter_consumer_secret = '" + twitter_consumer_secret + "', "
         sql = sql + "twitter_access_token = '" + twitter_access_token + "', "
         sql = sql + "twitter_access_secret = '" + twitter_access_secret + "';"

         exec_sql(conn,sql)

         sql = "update config set send_to_twitter = " + request.form["send_to_twitter"] + ", "
         sql = sql + "enable_aprs_msg_notify = " + request.form["enable_aprs_msg_notfiy"] + ", "
         sql = sql + "include_map_image = " + request.form["include_map_image"] + ";"
         
         exec_sql(conn,sql)        

         msg = request.form["app"].capitalize() + " Keys updated."

      except:
         conn.rollback()
         msg = "Error in Operation."

      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "telegram":

      header = "-------------------  " + request.form["app"].capitalize() + " API Keys -------------------"

      try:
         telegram_bot_token = request.form["telegram_bot_token"]
         telegram_my_chat_id = request.form["telegram_my_chat_id"]


         sql = "update apikeys set "
         sql = sql + "telegram_bot_token = '" + telegram_bot_token + "', "
         sql = sql + "telegram_my_chat_id = '" + telegram_my_chat_id + "';"

         exec_sql(conn,sql)

         sql = "update config set send_to_telegram = " + request.form["send_to_telegram"] + ";"
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mastodon":

      header = "-------------------  " + request.form["app"].capitalize() + " API Keys -------------------"

      try:

         mastodon_instance_url = request.form["mastodon_instance_url"]
         mastodon_bot_app_name = request.form["mastodon_bot_app_name"]
         mastodon_username = request.form["mastodon_username"]
         mastodon_password = request.form["mastodon_password"]

         client_keys = Mastodon.create_app(mastodon_bot_app_name, scopes=['read', 'write'], api_base_url=mastodon_instance_url)

         mastodon_api = Mastodon(client_keys[0], client_keys[1], api_base_url = mastodon_instance_url)

         access_token = mastodon_api.log_in(mastodon_username, mastodon_password, scopes=["read", "write"])

         sql = "update apikeys set "
         sql = sql + "mastodon_client_id = '" + client_keys[0] + "', "
         sql = sql + "mastodon_client_secret = '" + client_keys[1] + "', "
         sql = sql + "mastodon_api_base_url = '" + mastodon_instance_url + "', "
         sql = sql + "mastodon_user_access_token = '" + access_token + "';"

         exec_sql(conn,sql)

         sql = "update config set send_to_mastodon = " + request.form["send_to_mastodon"] + ";"
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " Keys updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "discord":

      header = "-------------------  " + request.form["app"].capitalize() + " Webhook -------------------"

      try:

         discord_webhook_url = request.form["discord_webhook_url"]

         sql = "update apikeys set "
         sql = sql + "discord_webhook_url = '" + discord_webhook_url + "';"

         exec_sql(conn,sql)

         sql = "update config set send_to_discord = " + request.form["send_to_discord"] + ";"
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " URL updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title)
         conn.close()

   if request.method == 'POST' and request.form["app"] == "mattermost":

      header = "-------------------  " + request.form["app"].capitalize() + " Webhook -------------------"

      try:

         mattermost_webhook_url = request.form["mattermost_webhook_url"]

         sql = "update apikeys set "
         sql = sql + "mattermost_webhook_url = '" + mattermost_webhook_url + "';"

         exec_sql(conn,sql)

         sql = "update config set send_to_mattermost = " + request.form["send_to_mattermost"] + ";"
         
         exec_sql(conn,sql)  

         msg = request.form["app"].capitalize() + " URL updated."
      except:
         conn.rollback()
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="smkeys", page_title = page_title)
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
         return render_template("results.html", msg = msg, header = header, page="otherapikeys", page_title = page_title)
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
         return render_template("results.html", msg = msg, header = header, page="otherapikeys", page_title = page_title)
         conn.close()

@app.route('/update_configs', methods = ['POST', 'GET'])
def update_configs():
   conn = create_connection(database)

   header = "-------------------  Configs Updated -------------------"

   try:

      sql = "update config set "
      sql = sql + "units_to_use = " + request.form["units_to_use"] + ", "
      sql = sql + "include_wx = " + request.form["include_wx"] + ", "
      sql = sql + "send_position_data = " + request.form["send_position_data"] + ", "
      sql = sql + "send_weather_data = " + request.form["send_weather_data"] + ";"

      exec_sql(conn,sql)

      msg = "Configurations settings updated."
   except:
      conn.rollback()
      msg = "Error in Operation."
   finally:
      return render_template("results.html", msg = msg, header = header, page="configuration", page_title = page_title)
      conn.close()

@app.route('/update_callsign_lists', methods = ['POST', 'GET'])
def update_callsign_lists():
   conn = create_connection(database)

   header = "-------------------  " + request.form["listtype"].upper() + " Callsign List -------------------"

   try:
      callsignlist = request.form["callsignlist"].split(",")
      listtype = request.form["listtype"] # POS, WX, Msg
      function = request.form["function"] # 1 = Add, 0 = delete

      if function == '1':
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
      return render_template("results.html", msg = msg, header = header, page="callsignlists", page_title = page_title)
      conn.close()


# Main Driver

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5001, debug=True)