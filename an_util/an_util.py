#!/usr/bin/env python3

######################################################################################################################
## Import Libraries
from flask import Flask, render_template, request
import os
import sys
from os import system, name
import sqlalchemy
from sqlalchemy import text as sqltext, select, MetaData, Table, distinct
import pytz

if os.path.exists('src'):
   # Import our Custom Libraries
   import src.db_functions as dbf
   import src.db_conn as dbc
else:
   current_dir = os.path.dirname(os.path.abspath(__file__))
   parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
   sys.path.insert(0, parent_dir)   

   import src.db_functions as dbf
   import src.db_conn as dbc  
#############################
# set database connection

try:
    db_engine = dbc.db_connection()
    print("Database Connection established")
except Exception as e:
    print("Database Connection could not be established.", e)

metadata = sqlalchemy.MetaData()
metadata.reflect(bind=db_engine)

config = metadata.tables['config']
apis = metadata.tables['apis']
services = metadata.tables['services']
callsignlist = metadata.tables['callsignlist']
supportedservices = metadata.tables['supportedservices']

######################################################################################################################
## define Variables
app = Flask(__name__)

linefeed = "\n"
html_linefeed = "<br>"

#Set Standard Page Title
page_title = "APRSNotify Configuration Utility"
wiki_link = "https://n8acl.github.io/aprsnotify/"
# page_title = Markup(page_title)

######################################################################################################################
## Define functions

def build_svc_url(formobj):
   if formobj['app'].lower() in ['discord','slack']:
      return formobj['service_url']
   elif formobj['app'].lower() == 'mastodon':
      return "mastodon://" + formobj['access_token'] + "@" + formobj['hostname']
   elif formobj['app'].lower() == 'telegram':
      return "tgram://" + formobj['bot_totken'] + "/" + formobj['chatid']
   elif formobj['app'].lower() == 'mattermost':
      return "mmost://" + formobj['hostname'] + "/" + formobj['webhook_token']
   elif formobj['app'].lower() == 'pushover':
      return "pover://" + formobj['userkey'] + "@" + formobj['api_token']
   elif formobj['app'].lower() == 'matrix':
      return "matrix://" + formobj['userkey'] + "@" + formobj['api_token']
   elif formobj['app'].lower() == 'dapnet':
      return "dapnet://" + formobj['username'] + ":" + formobj['password'] + "@" + formobj['callsign']
   elif formobj['app'].lower() == 'signal':
      return "signal://" + formobj['username'] + ":" + formobj['password'] + "@" + formobj['hostname'] + "/" + formobj['fromphoneno'] + "/" + formobj['target_chatid']


def add_svc_data(formobj):

   values_list = []

   if 'active' in formobj:
      active = True
   else:
      active = False

   if 'send_position_data' in formobj:
      send_position_data = True
   else:
      send_position_data = False

   if 'send_weather_data' in formobj:
      send_weather_data = True
   else:
      send_weather_data = False

   if 'send_message_data' in formobj:
      send_message_data = True
   else:
      send_message_data = False

   sql = services.insert()
   values_list = [{
      'service_name': formobj['app'],
      'friendlyname' : formobj["friendly_name"],
      'active': active,
      'service_url': build_svc_url(formobj),
      'send_pos_data': send_position_data,
      'send_wx_data': send_weather_data,
      'send_msg_data': send_message_data}]


   dbf.insert_sql(db_engine,sql,values_list)

def upd_svc_data(formobj):
   if 'active' in formobj:
      active = True
   else:
      active = False

   if 'send_position_data' in formobj:
      send_position_data = True
   else:
      send_position_data = False

   if 'send_weather_data' in formobj:
      send_weather_data = True
   else:
      send_weather_data = False

   if 'send_message_data' in formobj:
      send_message_data = True
   else:
      send_message_data = False

   sql = services.update().where((services.c.service_name == request.form["app"]) & (services.c.friendlyname == request.form["friendlyname"])).values(
      friendlyname = formobj["friendlyname"],
      active = active,
      service_url = build_svc_url(formobj),
      send_pos_data = send_position_data,
      send_wx_data = send_weather_data,
      send_msg_data = send_message_data
   )

   dbf.exec_sql(db_engine,sql)

def serviceslist():
      sql = sqlalchemy.select(supportedservices.c.service_name).order_by(supportedservices.c.service_name)

      return dbf.select_sql(db_engine,sql)

######################################################################################################################
## Define URL routes for Flask

#################### 
# Navigation Endpoints

@app.route('/')
def index():
   sql = sqlalchemy.select(config.c.setting_value_boolean).where(config.c.setting_name=='use_apprise_api')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      use_apprise_api = row[0]

   return render_template('index.html', use_apprise_api=use_apprise_api, page_title = page_title, wiki_link = wiki_link)

@app.route('/list_services')
def list_services():

   sql = sqlalchemy.select(services.c.service_name).distinct().order_by(services.c.service_name.asc())

   servicename_result = dbf.select_sql(db_engine,sql)

   sql = sqlalchemy.select(services.c.service_name,
   services.c.friendlyname,
   services.c.active,
   services.c.service_url,
   services.c.send_pos_data,
   services.c.send_wx_data,
   services.c.send_msg_data
   ).order_by(services.c.service_name.asc())

   services_result = dbf.select_sql(db_engine,sql) 

   return render_template('list_services.html', services_list = servicename_result, service_data = services_result, page_title = page_title, wiki_link = wiki_link)

@app.route('/configuration')
def configuration():

   sql = sqlalchemy.select(config.c.setting_value_int
   ).where(config.c.setting_name == 'units_to_use')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      units_to_use = row[0]

   sql = sqlalchemy.select(config.c.setting_value_int
   ).where(config.c.setting_name == 'delay_time')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      delay_time = row[0]

   sql = sqlalchemy.select(config.c.setting_value_boolean
   ).where(config.c.setting_name == 'use_apprise_api')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      use_apprise_api = row[0]

   sql = sqlalchemy.select(apis.c.apikey
   ).where(apis.c.apiname == 'aprsfi')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      aprsfi_apikey = row[0]

   sql = sqlalchemy.select(apis.c.apikey
   ).where(apis.c.apiname == 'wx_api')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      wx_apikey = row[0]

   sql = sqlalchemy.select(config.c.setting_value_text
   ).where(config.c.setting_name == 'user_timezone')

   result = dbf.select_sql(db_engine,sql)

   for row in result:
      user_timezone = row[0]
   
   timezones = []
   timezones = pytz.all_timezones

   return render_template('configuration.html', user_timezone=user_timezone, timezones=timezones, units_to_use=units_to_use, delay_time=delay_time, use_apprise_api = use_apprise_api, aprsfi_apikey = aprsfi_apikey, wx_apikey = wx_apikey, page_title = page_title, wiki_link = wiki_link)


@app.route('/callsignlists')
def callsignlists():

   sql = sqlalchemy.select(callsignlist.c.callsign,
   callsignlist.c.listtype
   ).order_by(callsignlist.c.callsign.asc(), callsignlist.c.listtype.asc())

   callsignlist_result = dbf.select_sql(db_engine,sql) 

   sql = sqlalchemy.select(callsignlist.c.callsign
   ).distinct().order_by(callsignlist.c.callsign.asc())

   del_callsign_list = dbf.select_sql(db_engine,sql) 

   return render_template('callsignlists.html', callsignlist = callsignlist_result, del_callsign_list = del_callsign_list, row_count=len(callsignlist_result), page_title = page_title, wiki_link = wiki_link)

@app.route('/add_services', methods = ['POST', 'GET'])
def add_services():
   return render_template("add_services.html", supportedservices = serviceslist(), page_title = page_title, wiki_link = wiki_link)


@app.route('/add_new_services', methods = ['POST', 'GET'])
def add_new_services():

   if request.method == 'POST':
      return render_template("add_servicedata.html", service_name=request.form["service_name"].capitalize(), page_title = page_title, wiki_link = wiki_link)
   return "Test"

@app.route('/update_services', methods = ['POST', 'GET'])
def update_services():

   if request.method == 'POST':

      sql = sqlalchemy.select(services.c.service_name,
      services.c.friendlyname,
      services.c.active,
      services.c.service_url,
      services.c.send_pos_data,
      services.c.send_wx_data,
      services.c.send_msg_data
      ).where((services.c.service_name == request.form["app"].lower()) & (services.c.friendlyname == request.form["friendlyname"]))

      service_data_result = dbf.select_sql(db_engine,sql)

      return render_template("update_servicedata.html", service_name=request.form["app"].capitalize(), service_data = service_data_result, page_title = page_title, wiki_link = wiki_link)
   return "Test"

@app.route('/apprise_api', methods = ['POST', 'GET'])
def apprise_api():

   sql = sqlalchemy.select(config.c.setting_value_text).where((config.c.setting_name == 'apprise_api_pos_tags'))

   apprise_api_pos_tags_result = dbf.select_sql(db_engine,sql)

   for row in apprise_api_pos_tags_result:
      apprise_api_pos_tags = row[0]

   sql = sqlalchemy.select(config.c.setting_value_text).where((config.c.setting_name == 'apprise_api_msg_tags'))

   apprise_api_msg_tags_result = dbf.select_sql(db_engine,sql)

   for row in apprise_api_msg_tags_result:
      apprise_api_msg_tags = row[0]

   sql = sqlalchemy.select(config.c.setting_value_text).where((config.c.setting_name == 'apprise_api_wx_tags'))

   apprise_api_wx_tags_result = dbf.select_sql(db_engine,sql)

   for row in apprise_api_wx_tags_result:
      apprise_api_wx_tags = row[0]

   sql = sqlalchemy.select(apis.c.apikey).where((apis.c.apiname == 'apprise_api'))

   apprise_apikey_result = dbf.select_sql(db_engine,sql)

   for row in apprise_apikey_result:
      apprise_apikey = row[0]

   sql = sqlalchemy.select(apis.c.apiurl).where((apis.c.apiname == 'apprise_api'))

   apprise_apiurl_result = dbf.select_sql(db_engine,sql)

   for row in apprise_apiurl_result:
      apprise_apiurl = row[0]

   return render_template("apprise_api.html", apprise_api_pos_tags = apprise_api_pos_tags, apprise_api_msg_tags = apprise_api_msg_tags, apprise_api_wx_tags = apprise_api_wx_tags, apprise_apikey = apprise_apikey, apprise_apiurl = apprise_apiurl, page_title = page_title, wiki_link = wiki_link)

#################### 
# Form Processing endpoints

@app.route('/add_service_data', methods = ['POST', 'GET'])
def add_service_data():

   if request.method == 'POST':

      header = "-------------------  " +  request.form['app'] + " - " + request.form['friendly_name'] + " -------------------"

      try:

         add_svc_data(request.form)

         msg = request.form['app'] + " - " + request.form['friendly_name'] + " settings added."
      except Exception as e:
         print(e)
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="serviceadd", page_title = page_title, wiki_link = wiki_link)

   return "Test"

@app.route('/update_service_data', methods = ['POST', 'GET'])
def update_service_data():

   if request.method == 'POST':

      header = "-------------------  " +  request.form['app'] + " - " + request.form['friendlyname'] + " -------------------"

      try:

         upd_svc_data(request.form)

         msg = request.form['app'] + " - " + request.form['friendlyname'] + " settings updated."
      except Exception as e:
         print(e)
         msg = "Error in Operation."
      finally:
         return render_template("results.html", msg = msg, header = header, page="serviceupdate", page_title = page_title, wiki_link = wiki_link)

   return "Test"

@app.route('/update_configs', methods = ['POST', 'GET'])
def update_configs():
   header = "-------------------  Configs Updated -------------------"

   try:

      if int(request.form['delay_time']) < 600:
         delay_time = 600
      else:
         delay_time = int(request.form['delay_time'])

      sql = config.update().where(config.c.setting_name == 'units_to_use').values(setting_value_int = int(request.form['units_to_use']))

      dbf.exec_sql(db_engine,sql)

      sql = config.update().where(config.c.setting_name == 'delay_time').values(setting_value_int = delay_time)

      dbf.exec_sql(db_engine,sql)

      sql = config.update().where(config.c.setting_name == 'user_timezone').values(setting_value_text = request.form['timezone'])

      dbf.exec_sql(db_engine,sql)

      if 'use_apprise_api' in request.form:
         use_apprise_api = True
      else:
         use_apprise_api = False

      sql = config.update().where(config.c.setting_name == 'use_apprise_api').values(setting_value_boolean = use_apprise_api)

      dbf.exec_sql(db_engine,sql)

      sql = apis.update().where(apis.c.apiname == 'aprsfi').values(apikey = request.form['aprsfi_apikey'])

      dbf.exec_sql(db_engine,sql)

      sql = apis.update().where(apis.c.apiname == 'wx_api').values(apikey = request.form['wx_apikey'])

      dbf.exec_sql(db_engine,sql)

      msg = "Config settings updated."
   except Exception as e:
      print(e)
      msg = "Error in Operation."
   finally:
      return render_template("results.html", msg = msg, header = header, page="configuration", page_title = page_title, wiki_link = wiki_link)


@app.route('/update_callsign_lists', methods = ['POST', 'GET'])
def update_callsign_lists():

   values_list = []

   header = "------------------- Callsign List -------------------"

   try:
      if request.form['submit'] == 'Add':
         if int(request.form['rowcount']) < 20:
            sql = sqlalchemy.select(callsignlist.c.callsign).where((callsignlist.c.callsign == request.form['callsign'].upper()) & (callsignlist.c.listtype == request.form['addtype'].upper()))

            callsignlist_result = dbf.select_sql(db_engine,sql)

            if len(callsignlist_result) > 0:
               msg = "Callsign already exists. Not added."
            else:
               sql = callsignlist.insert()
               values_list = [{
                  'callsign': request.form['callsign'].upper(),
                  'listtype': request.form['addtype'].upper(),
                  'last_timestamp': 0
               }]

               dbf.insert_sql(db_engine,sql,values_list)
               
               msg = "Callsign Added."
         else:
            msg = "Maximum number of callsigns reached."

      elif request.form['submit'] == 'Delete':
         sql = callsignlist.delete().where((callsignlist.c.callsign == request.form['del_call'].upper()) & (callsignlist.c.listtype == request.form['deltype'].upper()))

         dbf.exec_sql(db_engine,sql)
      
         msg = "Callsign Deleted."

   except Exception as e:
      print(e)
      msg = "Error in Operation."

   finally:
      return render_template("results.html", msg = msg, header = header, page="callsignlists", page_title = page_title, wiki_link = wiki_link)

@app.route('/update_appriseapi', methods = ['POST', 'GET'])
def update_appriseapi():

   values_list = []

   header = "------------------- Apprise-API Settings -------------------"

   try:

      sql = config.update().where(config.c.setting_name == 'apprise_api_pos_tags').values(setting_value_text = request.form['apprise_pos_tags'])

      dbf.exec_sql(db_engine,sql)

      sql = config.update().where(config.c.setting_name == 'apprise_api_msg_tags').values(setting_value_text = request.form['apprise_msg_tags'])

      dbf.exec_sql(db_engine,sql)

      sql = config.update().where(config.c.setting_name == 'apprise_api_wx_tags').values(setting_value_text = request.form['apprise_wx_tags'])

      dbf.exec_sql(db_engine,sql)

      sql = apis.update().where(apis.c.apiname == 'apprise_api').values(apikey = request.form['apprise_apikey'])

      dbf.exec_sql(db_engine,sql)

      sql = apis.update().where(apis.c.apiname == 'apprise_api').values(apiurl = request.form['apprise_url'])

      dbf.exec_sql(db_engine,sql)

      msg = "Apprise-API settings updated."
   except Exception as e:
      print(e)
      msg = "Error in Operation."
   finally:
      return render_template("results.html", msg = msg, header = header, page="appriseapiupdate", page_title = page_title, wiki_link = wiki_link)

   return "Test"


# Main Driver

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5001, debug=True)