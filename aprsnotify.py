#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Current Version: 5.0
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Telegram: @Ravendos
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################

# Import our Libraries

import time
from time import sleep
import os
from os import system
import datetime
import sqlite3
import sys
from sqlite3 import Error

try:
    import requests
except ImportError:
    exit('This script requires the requests module\nInstall with: pip3 install requests')
try:
    import telegram
except ImportError:
    exit('This script requires the python-telegram-bot module\nInstall with: pip3 install python-telegram-bot')
try:
    import tweepy
    from tweepy import OAuthHandler
except ImportError:
    exit('This script requires the tweepy module\nInstall with: pip3 install tweepy')
try:
    from geopy.geocoders import Nominatim
except ImportError:
    exit('This script requires the geopy module\nInstall with: pip3 install geopy')
try:
    from mastodon import Mastodon
except ImportError:
    exit('This script requires the mastodon.py module\nInstall with: pip3 install mastodon.py')
try:
    from discord_webhook import DiscordWebhook
except ImportError:
    exit('This script requires the discord_webhook module\nInstall with: pip3 install discord_webhook')

######################################################################################################################
# Define Variables and static objects

degree_sign= u'\N{DEGREE SIGN}'
fixed_station = 0
aprsfi_api_base_url = "https://api.aprs.fi/api/get"
owm_api_base_url = "http://api.openweathermap.org/data/2.5/weather"
geolocator = Nominatim(user_agent="aprstweet")
db_file = os.path.dirname(os.path.abspath(__file__)) + "/aprsnotify.db"
linefeed = "\n"
pos_callsign_list = []
msg_callsign_list = []
wx_callsign_list = []
goodposdata = 0
goodmsgdata = 0
goodwxdata = 0
debug = 0

######################################################################################################################
# Define Functions

def create_connection(db_file):
    # Creates connection to APRSNotify.db SQLlite3 Database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def select_sql(conn,sql):
    # Executes SQL for Selects
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_api_data(url,payload):
    # get JSON data from api's
    return requests.get(url=url,params=payload)

def get_curr_wx(lat, lon):
    # Return Conditions and Temp for the packet location.
    if units_to_use == 1:
        units = 'metric'
    else:
        units = 'imperial'

    owm_payload = {
        'lat': lat,
        'lon': lon,
        'units': units,
        'appid': openweathermapkey
    }
    
    data = get_api_data(owm_api_base_url,owm_payload)
    return data.json().get('weather')[0]['main'], data.json().get('main').get('temp') # Conditions, temp

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

def send_status(msg, msg_type, lat,lng):
    # msg_types
    # 1: Postion Data
    # 2: Weather Data
    # 3: APRS message

    # Create status for microblogs (Twitter, Mastodon)
    micro_status = msg + " #APRS"

    # Send status to various services
    if (send_to_twitter == 1): # Send Status to Twitter
        auth = OAuthHandler(twitterkeys["consumer_key"], twitterkeys["consumer_secret"])
        auth.set_access_token(twitterkeys["access_token"], twitterkeys["access_secret"])
        twitter_api = tweepy.API(auth)
        twitter_api.update_status(micro_status)

    if (send_to_telegram == 1): # Send Status to Telegram
        tele_bot_message(msg, msg_type)

    if (send_to_mastodon == 1): # Send Status to Mastodon
        mastodon_api = Mastodon(mastodonkeys["client_id"], mastodonkeys["client_secret"], mastodonkeys["user_access_token"], api_base_url=mastodonkeys["api_base_url"])
        mastodon_api.toot(micro_status)

    if (send_to_discord == 1): # Send Status to Discord
        webhook = DiscordWebhook(url=discord_wh_url, content=msg)
        response = webhook.execute()    


def tele_bot_message(msg, msg_type):
    # msg_types
    # 1: Postion Data
    # 2: Weather Data
    # 3: APRS message

    # Sends the message text to Telegram. This is used for both status and message sending
    bot = telegram.Bot(token=telegramkeys["my_bot_token"])
    bot.sendMessage(chat_id=telegramkeys["my_chat_id"], text=msg)
    if (include_map_image == 1 and msg_type not in [2,3]): # Includes a map of the packet location in Telegram
        bot.sendLocation(chat_id=telegramkeys["my_chat_id"], latitude=lat, longitude=lng, disable_notification=True)


######################################################################################################################
# Check for first run

if not os.path.exists(db_file):
    print(linefeed + "******** Your Database for APRSNotify is not configured. Please run an_util.py ********" + linefeed)
    sys.exit()
# else:
#     if os.path.exists(setup):
#         os.remove(setup)


######################################################################################################################
# Load Data from Database into variables

# Create Database Connection
conn = create_connection(db_file)

# Build Position Callsign list
result = select_sql(conn, "select callsign from callsignlists where listtype = 'POS';")

for row in result:
    pos_callsign_list.append(row[0])

# Build Message Callsign list
result = select_sql(conn, "select callsign from callsignlists where listtype = 'MSG';")

for row in result:
    msg_callsign_list.append(row[0])

# Build Weather Station Callsign list
result = select_sql(conn, "select callsign from callsignlists where listtype = 'WX';")

for row in result:
    wx_callsign_list.append(row[0])

# Get api keys from database

sql = """select 
twitter_consumer_key,
twitter_consumer_secret,
twitter_access_token,
twitter_access_secret,
telegram_bot_token,
telegram_my_chat_id,
aprsfikey,
openweathermapkey,
mastodon_client_id,
mastodon_client_secret,
mastodon_api_base_url,
mastodon_user_access_token,
discord_webhook_url,
mattermost_webhook_url
from apikeys"""

result = select_sql(conn, sql)

for row in result:
    twitterkeys = {
        "consumer_key": row[0],
        "consumer_secret": row[1],
        "access_token": row[2],
        "access_secret": row[3]
    }

    telegramkeys = {
        "my_bot_token": row[4], 
        "my_chat_id": row[5]
    }

    mastodonkeys = {
        "client_id": row[8],
        "client_secret": row[9],
        "api_base_url": row[10],
        "user_access_token": row[11]
    }

    aprsfikey = row[6]
    openweathermapkey = row[7]
    discord_wh_url = row[12]
    mm_wh_url = row[13]

# Get config switches from database

sql = """select 
    send_to_twitter,
    send_to_telegram,
    send_to_mastodon,
    units_to_use,
    enable_aprs_msg_notify,
    include_map_image,
    include_wx,
    send_position_data,
    send_weather_data,
    send_to_discord,
    send_to_mattermost
from config"""

result = select_sql(conn, sql)

for row in result:
    send_to_twitter = row[0]
    send_to_telegram = row[1]
    send_to_mastodon = row[2]
    units_to_use = row[3]
    enable_aprs_msg_notify = row[4]
    include_map_image = row[5]
    include_wx = row[6]
    send_position_data = row[7]
    send_weather_data = row[8]
    send_to_discord = row[9]
    send_to_mattermost = row[10]

# Get stamp data from database
sql = """select 
    lastpostime,
    lastmsgid,
    lastwxtime
from aprsstamps"""

result = select_sql(conn, sql)

for row in result:
    lasttime = row[0]
    lastmsgid = row[1]
    lastwxtime = row[2]

######################################################################################################################
# Define static JSON Payloads for API retrevial

position_payload = {
    'name': ",".join(pos_callsign_list),
    'what': 'loc',
    'apikey': aprsfikey,
    'format': 'json'
}

msg_payload = {
    'what': 'msg',
    'dst': ",".join(msg_callsign_list),
    'apikey': aprsfikey,
    'format': 'json'
}

wx_payload = {
    'name': ",".join(wx_callsign_list),
    'what': 'wx',
    'apikey': aprsfikey,
    'format': 'json'
}

######################################################################################################################
# Main Program

###########################################
# Check for position data

if send_position_data == 1:

    data = get_api_data(aprsfi_api_base_url,position_payload)

    x=0
    while x <= len(pos_callsign_list)-1 and x < data.json().get('found'):
        if int(data.json().get('entries')[x]["lasttime"]) > lasttime:
            station = data.json().get('entries')[x]["name"]
            lat = str(data.json().get('entries')[x]["lat"])
            lng = str(data.json().get('entries')[x]["lng"])
            lasttime = data.json().get('entries')[x]["lasttime"]
            if "speed" in data.json().get('entries')[x]:
                speedkph = float(data.json().get('entries')[x]["speed"])
            else:
                fixed_station = 1
        
            goodposdata = 1
            break
        else:
            x=x+1
            goodposdata = 0

    if goodposdata == 1: # If we have a good set of packet data
        
        #Create Status Message
        status = station + ": "+ get_location(lat,lng)
            
        if fixed_station == 0:
            if units_to_use == 1:
                status = status + " | Speed: "+ str(speedkph) + " kph"
            else:
                status = status + " | Speed: "+ str(round(speedkph/1.609344,1)) + " mph"  
            
        status = status + " | Grid: " + get_grid(float(lat),float(lng))
        
        if include_wx == 1:
            #Get Weather Information
            conditions, temp = get_curr_wx(lat, lng)

            if units_to_use == 1:
                status = status + " | WX: "+ str(temp) + degree_sign + " C & " + conditions
            else:
                status = status + " | WX: "+ str(temp) + degree_sign + " F & " + conditions

        status = status + " | " + datetime.datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S') + \
            " | https://aprs.fi/" + station
        
        if debug == 0:
            send_status(status,1,lat,lng) # Send status to Social Networks
        else:
            #send_status(status,lat,lng) # Send status to Social Networks
            print(status) # Send to Screen (for debugging)

###########################################
# Now check for Weather Station Data  
      
if send_weather_data == 1:

    data = get_api_data(aprsfi_api_base_url,wx_payload)

    x=0
    while x <= len(wx_callsign_list)-1 and x < data.json().get('found'):
        if int(data.json().get('entries')[x]["time"]) > lastwxtime:
            station = data.json().get('entries')[x]["name"]
            lastwxtime = data.json().get('entries')[x]["time"]
            if "temp" in data.json().get('entries')[x]:
                tempC = float(data.json().get('entries')[x]["temp"])
            else:
                tempC = 'None'
            if "pressure" in data.json().get('entries')[x]:
                pressure = float(data.json().get('entries')[x]["pressure"])
            else:
                pressure = 'None'            
            if "humidity" in data.json().get('entries')[x]:
                humidity = float(data.json().get('entries')[x]["humidity"])
            else:
                humidity = 'None' 
            if "wind_direction" in data.json().get('entries')[x]:
                wind_direction = float(data.json().get('entries')[x]["wind_direction"])
            else:
                wind_direction = 'None'
            if "wind_speed" in data.json().get('entries')[x]:
                wind_speed = float(data.json().get('entries')[x]["wind_speed"])
            else:
                wind_speed = 'None'
            if "wind_gust" in data.json().get('entries')[x]:
                wind_gust = float(data.json().get('entries')[x]["wind_gust"])
            else:
                wind_gust = 'None'
            if "rain_1h" in data.json().get('entries')[x]:
                rain_1h = float(data.json().get('entries')[x]["rain_1h"])
            else:
                rain_1h = 'None'
            if "rain_24h" in data.json().get('entries')[x]:
                rain_24h = float(data.json().get('entries')[x]["rain_24h"])
            else:
                rain_24h = 'None'
            if "rain_mn" in data.json().get('entries')[x]:
                rain_mn = float(data.json().get('entries')[x]["rain_mn"])
            else:
                rain_mn = 'None'
            if "luminosity" in data.json().get('entries')[x]:
                luminosity = float(data.json().get('entries')[x]["luminosity"])
            else:
                luminosity = 'None'

            goodwxdata = 1
            break
        else:
            x=x+1
            goodwxdata = 0

    if goodwxdata == 1: # If we have a good set of packet data
        
        #Create Status Message
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

        # status = status + "Time: " +  datetime.datetime.fromtimestamp(int(lastwxtime)).strftime('%H:%M:%S') + " | " + \
        status = status + "https://aprs.fi/" + station
        
        if debug == 0:
            send_status(status,2,lat,lng) # Send status to Social Networks
        else: 
            print(status) # Send to Screen (for debugging)

###########################################
# Now Check for messages to my callsign(s) 

if enable_aprs_msg_notify == 1:

    data = get_api_data(aprsfi_api_base_url,msg_payload)

    x=0
    while x <= len(msg_callsign_list)-1 and x < data.json().get('found'):
        if int(data.json().get('entries')[x]["messageid"]) > lastmsgid:
            srccall = data.json().get('entries')[x]["srccall"]
            dstcall = data.json().get('entries')[x]["dst"]
            msg = data.json().get('entries')[x]["message"]
            dtstamp = data.json().get('entries')[x]["time"]
            lastmsgid = data.json().get('entries')[x]["messageid"]
            goodmsgdata = 1
            break
        else:
            x=x+1
            goodmsgdata = 0

    if goodmsgdata == 1: # If we have good msg data
        msg_timestamp = datetime.datetime.fromtimestamp(int(dtstamp)).strftime('%H:%M:%S')
        msg_datestamp = datetime.datetime.fromtimestamp(int(dtstamp)).strftime('%m/%d/%Y')

        # create msg status and send to Telegram
        msg_status = "On " + msg_datestamp + " at " + msg_timestamp + " " + srccall + " sent " + dstcall + " the following APRS message: " + linefeed + msg
        if debug == 0:
            tele_bot_message(msg_status,3)
        else:
            print(msg_status) # Send to Screen (for debugging)

# Update aprsstamps table in database with lastmsgid/DT Stamp and close
sql = "update aprsstamps set lastpostime = " + str(lasttime) + ", lastmsgid = " + str(lastmsgid) + ", lastwxtime = " + str(lastwxtime) + ";"
if debug == 0:
    exec_sql(conn, sql)
else:
    print(sql)