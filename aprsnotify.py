#!/usr/bin/env python3
#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Current Version: 2.0
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Discord: Ravendos
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################


######################################################################################################################
# Import Python Libraries

import time
from time import sleep
import os
from os import system
import requests
import datetime
from datetime import datetime
import pytz
import sys
import json
import http.client, urllib
import sqlalchemy
from sqlalchemy import text as sqltext, select, MetaData, Table
from geopy.geocoders import Nominatim
import apprise

# Import our Custom Libraries
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

######################################################################################################################
## Define Static Variables and static objects

degree_sign= u'\N{DEGREE SIGN}'
geolocator = Nominatim(user_agent="aprsnotify")
apobj = apprise.Apprise() # Apprise Object
linefeed = "\n"
pos_callsign_list = []
msg_callsign_list = []
wx_callsign_list = []
fixed_station = False
server_timezone = "Etc/UTC"
localFormat = "%Y-%m-%d %H:%M:%S"
localFormat_time = "%H:%M:%S"
localFormat_date = "%Y-%m-%d"

######################################################################################################################
## Define Functions

def get_api_data(url):
    # get JSON data from api's with just a URL
    return requests.get(url=url).json()

def get_api_data_payload(url,payload):
    # get JSON data from api's with payload
    try:
        responses = requests.get(url=url,params=payload).json()
    except ValueError as e:
        return 0
    return responses

def get_curr_wx(lat,lon):
    # Return Conditions and Temp for the WX

    # Weather API URL
    sql = sqlalchemy.select(apis.c.apiurl).where(apis.c.apiname=='wx_api')

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        wx_url = row[0]

    # Weather API Key

    sql = sqlalchemy.select(apis.c.apikey).where(apis.c.apiname=='wx_api')

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        wxkey = row[0]

    wx_api_payload = {
            'key': wxkey,
            'q': str(lat) + "," + str(lon)
    }

    forecast = get_api_data_payload(wx_url,wx_api_payload)
    conditions = forecast["current"]["condition"]["text"]
    temp = forecast["current"]["temp_f"]

    return conditions, temp

def get_location(lat,lng):
    # Reverse geocode with openstreetmaps for location
    osm_address = geolocator.reverse(lat.strip()+","+lng.strip())
    return osm_address.address

def get_grid(dec_lat, dec_lon):
    ## Function developed by Walter Underwood, K6WRU https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square
    # Returns the Grid Square for the packet location

    upper = 'ABCDEFGHIJKLMNOPQRSTUVWX'
    lower = 'abcdefghijklmnopqrstuvwx'

    if not (-180<=dec_lon<180):
        sys.stderr.write('longitude must be -180<=lon<180, given %f\n'%dec_lon)
        sys.exit(32)
    if not (-90<=dec_lat<90):
        sys.stderr.write('latitude must be -90<=lat<90, given %f\n'%dec_lat)
        sys.exit(33) # can't handle north pole, sorry, [A-R]

    adj_lat = dec_lat + 90.0
    adj_lon = dec_lon + 180.0

    grid_lat_sq = upper[int(adj_lat/10)]
    grid_lon_sq = upper[int(adj_lon/20)]

    grid_lat_field = str(int(adj_lat%10))
    grid_lon_field = str(int((adj_lon/2)%10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon/2)*2) * 60

    grid_lat_subsq = lower[int(adj_lat_remainder/2.5)]
    grid_lon_subsq = lower[int(adj_lon_remainder/5)]

    return grid_lon_sq + grid_lat_sq + grid_lon_field + grid_lat_field + grid_lon_subsq + grid_lat_subsq

def build_callsignlist(ltype):

    callsign_list = []

    sql = sqlalchemy.select(callsignlist.c.callsign).where((callsignlist.c.listtype==ltype))

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        callsign_list.append(row[0])

    return callsign_list

def get_last_timestamp(callsign,ltype):

    sql = sqlalchemy.select(callsignlist.c.last_timestamp).where((callsignlist.c.listtype==ltype) & (callsignlist.c.callsign==callsign))

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        last_timestamp = row[0]

    return last_timestamp

def update_last_timestamp(callsign,ltype,last_timestamp):

    sql = callsignlist.update().where((callsignlist.c.callsign==callsign) & (callsignlist.c.listtype==ltype)).values(last_timestamp=last_timestamp)

    dbf.exec_sql(db_engine,sql)

def convert_local_time(timevar):
    timestamp_naive = datetime.fromtimestamp(timevar)
    timestamp_moment = timestamp_naive.astimezone(pytz.utc)
    return timestamp_moment.astimezone(pytz.timezone(user_timezone))

def send_msg_api(tag, msg, title):

    # get Apprise-api url

    sql = sqlalchemy.select(apis.c.apikey, apis.c.apiurl).where(apis.c.apiname=='apprise_api')

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        apprise_api_url = row[1] + row[0]

    # get Apprise-api tags to send to

    sql = sqlalchemy.select(config.c.setting_value_text).where(config.c.setting_name=='apprise_api_'+tag.lower()+'_tags')

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        tags = row[0]
    

    payload = {
    'tag': tags,
    'title': title,
    'body': msg
    }

    response = requests.post(
        apprise_api_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"} 
    )
        

def send_msg(apobj, tag, msg, title):

    apobj.notify(
        body=msg,
        title=title,
        tag=tag
    )

######################################################################################################################
## Define Dynamic Variables from Database

# Set delay time for checking for Packet information

sql = sqlalchemy.select(config.c.setting_value_int).where(config.c.setting_name =='delay_time')

result = dbf.select_sql(db_engine,sql)

for row in result:
    delay_time = row[0]

# APRSFI APi URL
sql = sqlalchemy.select(apis.c.apiurl).where(apis.c.apiname=='aprsfi')

result = dbf.select_sql(db_engine,sql)

for row in result:
    aprsfi_url = row[0]

# APRSFi API Key

sql = sqlalchemy.select(apis.c.apikey).where(apis.c.apiname=='aprsfi')

result = dbf.select_sql(db_engine,sql)

for row in result:
    aprsfikey = row[0]

# Set Units to use

sql = sqlalchemy.select(config.c.setting_value_int).where(config.c.setting_name=='units_to_use')

result = dbf.select_sql(db_engine,sql)

for row in result:
    units_to_use = row[0]

# Get User's Timezone

sql = sqlalchemy.select(config.c.setting_value_text).where(config.c.setting_name=='user_timezone')

result = dbf.select_sql(db_engine,sql)

for row in result:
    user_timezone = row[0]

## Set Apprise Object

# First check to see if we are using the Apprise-API

sql = sqlalchemy.select(config.c.setting_value_boolean).where(config.c.setting_name=='use_apprise_api')

result = dbf.select_sql(db_engine,sql)

for row in result:
    use_apprise_api = row[0]

# Now build the objects appropriatly

if not use_apprise_api:
    # Build the Apprise Object for native install
    # Position Services
    sql = sqlalchemy.select(services.c.service_url).where((services.c.active==True) & (services.c.send_pos_data==True))

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        apobj.add(row[0], tag='POS')

    # Weather Services
    sql = sqlalchemy.select(services.c.service_url).where((services.c.active==True) & (services.c.send_wx_data==True))

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        apobj.add(row[0], tag='WX')

    # Messaging Services
    sql = sqlalchemy.select(services.c.service_url).where((services.c.active==True) & (services.c.send_msg_data==True))

    result = dbf.select_sql(db_engine,sql)

    for row in result:
        apobj.add(row[0], tag='MSG')

######################################################################################################################
# Define static JSON Payloads for API retrevials

aprsfi_position_payload = {
    'name': ",".join(build_callsignlist('POS')),
    'what': 'loc',
    'apikey': aprsfikey,
    'format': 'json'
}

aprsfi_msg_payload = {
    'what': 'msg',
    'dst': ",".join(build_callsignlist('MSG')),
    'apikey': aprsfikey,
    'format': 'json'
}

aprs_wx_payload = {
    'name': ",".join(build_callsignlist('WX')),
    'what': 'wx',
    'apikey': aprsfikey,
    'format': 'json'
}

######################################################################################################################
# Main Program

while True:

    # Check for Position Data
    if len(build_callsignlist('POS')) > 0:
        data = get_api_data_payload(aprsfi_url,aprsfi_position_payload)

        for x in range(0,data['found']):
            fixed_station = False

            if int(data['entries'][x]["lasttime"]) > get_last_timestamp(data['entries'][x]["name"],'POS'):
                station = data['entries'][x]["name"]
                lat = str(data['entries'][x]["lat"])
                lng = str(data['entries'][x]["lng"])
                lasttime = data['entries'][x]["lasttime"]
                if "speed" in data['entries'][x]:
                    speedkph = float(data['entries'][x]["speed"])
                else:
                    fixed_station = True

                status = station + ": "+ get_location(lat,lng)
                    
                if not fixed_station:
                    if units_to_use == 1:
                        status = status + " | Speed: "+ str(speedkph) + " kph"
                    else:
                        status = status + " | Speed: "+ str(round(speedkph/1.609344,1)) + " mph"  
                    
                status = status + " | Grid: " + get_grid(float(lat),float(lng))
                
                #Get Weather Data
                conditions, temp = get_curr_wx(lat, lng)

                if units_to_use == 1:
                    status = status + " | WX: "+ str(temp) + degree_sign + " C & " + conditions
                else:
                    status = status + " | WX: "+ str(temp) + degree_sign + " F & " + conditions

                status = status + " | " + convert_local_time(int(lasttime)).strftime(localFormat_time)

                # Now finish off the status for Slack and everything else. The URL create method is different for Slack
                status = status +  " | https://aprs.fi/" + station + " #APRS"
                title = station + ' Position Report'

                if use_apprise_api:
                    send_msg_api('POS', status, title)
                else:
                    send_msg(apobj, 'POS', status, title)

                update_last_timestamp(station,'POS', lasttime)

    # Check for Weather Data

    if len(build_callsignlist('WX')) > 0:
        data = get_api_data_payload(aprsfi_url,aprsfi_wx_payload)

        for x in range(0,data['found']):
            if int(data['entries'][x]["time"]) > get_last_timestamp(data['entries'][x]["name"],'WX'):
                station = data['entries'][x]["name"]
                lastwxtime = data['entries'][x]["time"]
                if "temp" in data['entries'][x]:
                    tempC = float(data['entries'][x]["temp"])
                else:
                    tempC = 'None'
                if "pressure" in data['entries'][x]:
                    pressure = float(data['entries'][x]["pressure"])
                else:
                    pressure = 'None'            
                if "humidity" in data['entries'][x]:
                    humidity = float(data['entries'][x]["humidity"])
                else:
                    humidity = 'None' 
                if "wind_direction" in data['entries'][x]:
                    wind_direction = float(data['entries'][x]["wind_direction"])
                else:
                    wind_direction = 'None'
                if "wind_speed" in data['entries'][x]:
                    wind_speed = float(data['entries'][x]["wind_speed"])
                else:
                    wind_speed = 'None'
                if "wind_gust" in data['entries'][x]:
                    wind_gust = float(data['entries'][x]["wind_gust"])
                else:
                    wind_gust = 'None'
                if "rain_1h" in data['entries'][x]:
                    rain_1h = float(data['entries'][x]["rain_1h"])
                else:
                    rain_1h = 'None'
                if "rain_24h" in data['entries'][x]:
                    rain_24h = float(data['entries'][x]["rain_24h"])
                else:
                    rain_24h = 'None'
                if "rain_mn" in data['entries'][x]:
                    rain_mn = float(data['entries'][x]["rain_mn"])
                else:
                    rain_mn = 'None'
                if "luminosity" in data['entries'][x]:
                    luminosity = float(data['entries'][x]["luminosity"])
                else:
                    luminosity = 'None'

                status = station + " WX Data as of " + datetime.datetime.fromtimestamp(int(lastwxtime)).strftime('%H:%M:%S') + linefeed

                if isinstance(tempC,float):
                    if units_to_use == 1:
                        status = status + "Temp: " + str(tempC) + degree_sign + " C" + linefeed
                    else:
                        status = status + "Temp: " + str(9.0/5.0 * tempC + 32) + degree_sign + " F" + linefeed
                if isinstance(pressure,float):
                    status = status + "Pressure: " + str(pressure) + " mbar" + linefeed
                if isinstance(humidity,float):
                    status = status + "Humidity: " + str(humidity) + "%" + linefeed
                if isinstance(wind_direction,float):
                    status = status + "Wind Direction: " + str(wind_direction) + degree_sign + linefeed
                if isinstance(wind_speed,float):
                    if units_to_use == 1:
                        status = status + "Wind Speed: " + str(round(wind_speed * 3.6,1)) + " kph" + linefeed
                    else:
                        status = status + "Wind Speed: " + str(round(wind_speed * 2.2369,1)) + " mph" + linefeed
                if isinstance(wind_gust,float):
                    if units_to_use == 1:
                        status = status + "Wind Gust: " + str(round(wind_gust * 3.6,1)) + " kph" + linefeed
                    else:
                        status = status + "Wind Gust: " + str(round(wind_gust * 2.2369,1)) + " mph" + linefeed
                if isinstance(rain_1h,float):
                    if units_to_use == 1:
                        status = status + "Rain 1Hr: " + str(round(rain_1h,1)) + " mm" + linefeed
                    else:
                        status = status + "Rain 1Hr: " + str(round(rain_1h * 0.03937007874,1)) + " in" + linefeed
                if isinstance(rain_24h,float):
                    if units_to_use == 1:
                        status = status + "Rain 24Hr: " + str(round(rain_24h,1)) + " mm" + linefeed
                    else:
                        status = status + "Rain 24Hr: " + str(round(rain_24h * 0.03937007874,1)) + " in" + linefeed
                if isinstance(rain_24h,float):
                    if units_to_use == 1:
                        status = status + "Rain Since Midnight: " + str(round(rain_mn,1)) + " mm" + linefeed
                    else:
                        status = status + "Rain Since Midnight: " + str(round(rain_mn * 0.03937007874,1)) + " in" + linefeed
                if isinstance(luminosity,float):
                    status = status + "Luminosity: " + str(luminosity) + "W/m^2" + linefeed

                # Now finish off the status for Slack and everything else. The URL create method is different for Slack
                status = status +  " | https://aprs.fi/" + station + " #APRS"
                title = station + ' Weather Report'

                if use_apprise_api:
                    send_msg_api('WX', status, title)
                else:
                    send_msg(apobj, 'WX', status, title)

                update_last_timestamp(station,'WX', lastwxtime)

    # Check for Message Data

    if len(build_callsignlist('MSG')) > 0:
        data = get_api_data_payload(aprsfi_url,aprsfi_msg_payload)

        for x in range(0,data['found']):
            if int(data['entries'][x]["messageid"]) > get_last_timestamp(data['entries'][x]["dst"],'MSG'):
                srccall = data['entries'][x]["srccall"]
                dstcall = data['entries'][x]["dst"]
                msg = data['entries'][x]["message"]
                dtstamp = data['entries'][x]["time"]
                lastmsgid = data['entries'][x]["messageid"]

                msg_timestamp = convert_local_time(int(dtstamp)).strftime(localFormat_time)
                msg_datestamp = convert_local_time(int(dtstamp)).strftime(localFormat_date)

                # create msg status and send to Telegram
                msg_status = "On " + msg_datestamp + " at " + msg_timestamp + ", " + srccall + " sent " + dstcall + " the following APRS message: " + msg
                title = "Message Notification"

                if use_apprise_api:
                    send_msg_api('MSG', msg_status, title)
                else:
                    send_msg(apobj, 'MSG', msg_status, title)

                update_last_timestamp(dstcall,'MSG', lastmsgid)  

    sleep(delay_time)          
