#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Current Version: 02032023
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################

# Import our Libraries

import time
import os
from os import system
import datetime
import sqlite3
import sys
import json
import http.client, urllib
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
    from geopy.geocoders import Nominatim
except ImportError:
    exit('This script requires the geopy module\nInstall with: pip3 install geopy')
try:
    from mastodon import Mastodon
except ImportError:
    exit('This script requires the mastodon.py module\nInstall with: pip3 install mastodon.py')
try:
    from discord_webhook import DiscordWebhook, DiscordEmbed
except ImportError:
    exit('This script requires the discord_webhook module\nInstall with: pip3 install discord_webhook')
try:
    from matterhook import Webhook
except ImportError:
    exit('This script requires the matterhook module\nInstall with: pip3 install matterhook')

######################################################################################################################
# Define Variables and static objects

degree_sign= u'\N{DEGREE SIGN}'
fixed_station = 0
aprsfi_api_base_url = "https://api.aprs.fi/api/get"
owm_api_base_url = "http://api.openweathermap.org/data/2.5/weather"
geolocator = Nominatim(user_agent="aprsnotify")
db_file = os.path.dirname(os.path.abspath(__file__)) + "/aprsnotify.db"
linefeed = "\n"
pos_callsign_list = []
msg_callsign_list = []
wx_callsign_list = []
goodposdata = False
goodmsgdata = False
goodwxdata = False
debug = False

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

def get_api_data(url):
    # get JSON data from api's with just a URL
    return requests.get(url=url).json()

def get_api_data_payload(url,payload):
    # get JSON data from api's
    try:
        responses = requests.get(url=url,params=payload).json()
    except ValueError as e:
        return 0
    return responses

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
    
    data = get_api_data_payload(owm_api_base_url,owm_payload)
    return data['weather'][0]['main'], data['main']['temp'] # Conditions, temp

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

def send_telegram(msg, msg_type, lat,lng, bot_token, chat_id):
    # msg_types
    # 1: Postion Data
    # 2: Weather Data
    # 3: APRS message

    # Sends the message text to Telegram. This is used for both status and message sending
    bot = telegram.Bot(token=bot_token)
    if msg_type in [1,2]:
        bot.sendMessage(chat_id=chat_id, text=msg)
    else:
        bot.sendMessage(chat_id=chat_id, text=msg)
    if (include_map_image_telegram == 1 and msg_type not in [2,3]): # Includes a map of the packet location in Telegram
        bot.sendLocation(chat_id=chat_id, latitude=lat, longitude=lng, disable_notification=True)

def send_mastodon(msg):

    mastodon_api = Mastodon(mastodonkeys["client_id"], mastodonkeys["client_secret"], mastodonkeys["user_access_token"], api_base_url=mastodonkeys["api_base_url"])
    mastodon_api.toot(micro_status)

def send_discord(msg,wh_url, msg_type, station):
    # webhook = DiscordWebhook(url=wh_url, content=msg)
    # response = webhook.execute() 

    if msg_type == 1:
        title = station + " Position Report"
    elif msg_type == 2:
        title = station + " Weather Report"
    elif msg_type == 3:
        title = "Message Notification"

    webhook = DiscordWebhook(url=wh_url)

    embed = DiscordEmbed(title=title, description=msg)
    webhook.add_embed(embed)

    response = webhook.execute() 

def send_mattermost(msg,wh_url, api_key):
    mm_bot = Webhook(mattermostwh["wh_url"], mattermostwh["apikey"])
    mm_bot.send(msg)  

def send_pushover(msg):
    connn = http.client.HTTPSConnection("api.pushover.net:443")
    connn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": pushover["pushover_token"],
        "user": pushover["pushover_userkey"],
        "message": msg,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    connn.getresponse()

def send_slack(msg,wh_url):
    response = requests.post(
        wh_url, data=json.dumps(msg),
        headers={'Content-Type': 'application/json'}
    )

######################################################################################################################
# Check for version arguement and return just the version

if len(sys.argv)>1:
    if sys.argv[1] == 'version':
        sql = "select version from config;"

        conn = create_connection(db_file)

        result = select_sql(conn, sql)
        for row in result:
            print("APRSNotify Release " + row[0])
        sys.exit()

######################################################################################################################


######################################################################################################################
# Check for first run

if not os.path.exists(db_file):
    print(linefeed + "******** Your Database for APRSNotify is not configured. Please run an_util.py ********" + linefeed)
    sys.exit()

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
telegram_bot_token,
telegram_poswx_chat_id,
aprsfikey,
openweathermapkey,
mastodon_client_id,
mastodon_client_secret,
mastodon_api_base_url,
mastodon_user_access_token,
discord_poswx_wh_url,
mattermost_poswx_wh_url,
mattermost_poswx_api_key,
discord_aprsmsg_wh_url,
pushover_token,
pushover_userkey,
slack_poswx_wh_url,
slack_aprsmsg_wh_url,
mattermost_aprsmsg_wh_url,
mattermost_aprsmsg_api_key,
telegram_aprsmsg_chat_id,
telegram_club_chat_id,
telegram_club_bot_token,
discord_club_wh_url,
mattermost_club_wh_url,
mattermost_club_api_key,
slack_club_wh_url
from apikeys"""

result = select_sql(conn, sql)

for row in result:
    telegramkeys = {
        "my_bot_token": row[0], 
        "poswx_chat_id": row[1],
        "aprsmsg_chat_id": row[18],
        "club_bot_token": row[20],
        "club_chat_id": row[19]
    }

    mastodonkeys = {
        "client_id": row[4],
        "client_secret": row[5],
        "api_base_url": row[6],
        "user_access_token": row[7]
    }

    discordwh = {
        "poswx_wh_url": row[8],
        "aprsmsg_wh_url": row[11],
        "club_wh_url": row[21]
    }

    mattermostwh = {
        "poswx_wh_url": row[9],
        "poswx_apikey": row[10],
        "msg_wh_url": row[16],
        "msg_apikey": row[17],
        "club_wh_url": row[22],
        "club_apikey": row[23]
    }

    pushover = {
        "pushover_token": row[12],
        "pushover_userkey": row[13]

    }

    slackwh = {
        "poswx_wh_url": row[14],
        "aprsmsg_wh_url": row[15],
        "club_wh_url": row[24]
    }


    aprsfikey = row[2]
    openweathermapkey = row[3]

# Get config switches from database

sql = """select 
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
    aprsmsg_notify_mattermost,
    aprsmsg_notify_slack,
    slack,
    club_telegram,
    club_discord,
    club_mattermost,
    club_slack
from config"""

result = select_sql(conn, sql)

for row in result:
    telegram = row[0]
    mastodon = row[1]
    discord = row[2]
    mattermost = row[3]
    units_to_use = row[4]
    include_map_image_telegram = row[5]
    include_wx = row[6]
    send_position_data = row[7]
    send_weather_data = row[8]
    aprsmsg_notify_telegram = row[9]
    aprsmsg_notify_discord = row[10]
    aprsmsg_notify_pushover = row[11]
    aprsmsg_notify_mattermost = row[12]
    aprsmsg_notify_slack = row[13]
    slack = row[14]
    club_telegram = row[15]
    club_discord = row[16]
    club_mattermost = row[17]
    club_slack = row[18]

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
# Define static JSON Payloads for API retrevials

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

if send_position_data:

    data = get_api_data_payload(aprsfi_api_base_url,position_payload)

    x=0
    while x <= len(pos_callsign_list)-1 and x < data['found']:
        if int(data['entries'][x]["lasttime"]) > lasttime:
            station = data['entries'][x]["name"]
            lat = str(data['entries'][x]["lat"])
            lng = str(data['entries'][x]["lng"])
            lasttime = data['entries'][x]["lasttime"]
            if "speed" in data['entries'][x]:
                speedkph = float(data['entries'][x]["speed"])
            else:
                fixed_station = True
        
            goodposdata = True
            break
        else:
            x=x+1
            goodposdata = False

    if goodposdata: # If we have a good set of packet data
        
        #Create Status Message
        status = station + ": "+ get_location(lat,lng)
            
        if not fixed_station:
            if units_to_use == 1:
                status = status + " | Speed: "+ str(speedkph) + " kph"
            else:
                status = status + " | Speed: "+ str(round(speedkph/1.609344,1)) + " mph"  
            
        status = status + " | Grid: " + get_grid(float(lat),float(lng))
        
        if include_wx:
            #Get Weather Data
            conditions, temp = get_curr_wx(lat, lng)

            if units_to_use == 1:
                status = status + " | WX: "+ str(temp) + degree_sign + " C & " + conditions
            else:
                status = status + " | WX: "+ str(temp) + degree_sign + " F & " + conditions

        status = status + " | " + datetime.datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S')

        # Now finish off the status for Slack and everything else. The URL create method is different for Slack
        slack_status = status + " | <https://aprs.fi/" + station + "|https://aprs.fi/" + station + ">"
        status = status +  " | https://aprs.fi/" + station
        micro_status = status + " #APRS" # for microblogging sites like Twitter/Mastodon

        msg_type = 1 # APRS Position Data
        
        # Now we send the status
        if not debug:
                # msg_types
                # 1: Postion Data
                # 2: Weather Data
                # 3: APRS message

            # Send to a personal system
            if telegram: # Send Status to Telegram
                send_telegram(status, msg_type, lat,lng, telegramkeys["my_bot_token"], telegramkeys["poswx_chat_id"])

            if mastodon: # Send Status to Mastodon
                send_mastodon(micro_status)

            if discord: # Send Status to Discord
                send_discord(status, discordwh["poswx_wh_url"], msg_type, station)

            if mattermost: # Send Status to Mattermost
                send_mattermost(status, mattermostwh["poswx_wh_url"], mattermostwh["poswx_apikey"])

            if slack: # Send Status to Slack
                slack_msg = {'text': slack_status}
                send_slack(slack_msg, slackwh["poswx_wh_url"])
            
            # See about sending to a club system            
            if club_telegram: # Send Status to Telegram
                send_telegram(status, 1, lat,lng, telegramkeys["club_bot_token"], telegramkeys["club_chat_id"])

            if club_discord: # Send Status to Discord
                send_discord(status, discordwh["club_wh_url"], msg_type, station)

            if club_mattermost: # Send Status to Mattermost
                send_mattermost(status, mattermostwh["club_wh_url"], mattermostwh["club_apikey"])

            if club_slack: # Send Status to Slack
                slack_msg = {'text': slack_status}
                send_slack(slack_msg, slackwh["club_wh_url"])
        else:
            print(status) # Send to Screen (for debugging)

###########################################
# Now check for Weather Station Data  
      
if send_weather_data:

    data = get_api_data_payload(aprsfi_api_base_url,wx_payload)

    x=0
    while x <= len(wx_callsign_list)-1 and x < data['found']:
        if int(data['entries'][x]["time"]) > lastwxtime:
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

            goodwxdata = True
            break
        else:
            x=x+1
            goodwxdata = False

    if goodwxdata: # If we have a good set of packet data
        
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

        # Now finish off the status for Slack and everything else. The URL create method is different for Slack
        slack_status = status + " | <https://aprs.fi/" + station + "|https://aprs.fi/" + station + ">"
        status = status +  " | https://aprs.fi/" + station

        msg_type = 2 # APRS Weather Data
        
        if not debug:
                # msg_types
                # 1: Postion Data
                # 2: Weather Data
                # 3: APRS message

            # Send to a personal system
            if telegram: # Send Status to Telegram
                send_telegram(status, msg_type, lat,lng, telegramkeys["my_bot_token"], telegramkeys["poswx_chat_id"])

            if mastodon: # Send Status to Mastodon
                send_mastodon(status)

            if discord: # Send Status to Discord
                send_discord(status, discordwh["poswx_wh_url"], msg_type, station)

            if mattermost: # Send Status to Mattermost
                send_mattermost(status, mattermostwh["poswx_wh_url"], mattermostwh["poswx_apikey"])

            if slack: # Send Status to Slack
                slack_msg = {'text': slack_status}
                send_slack(slack_msg, slackwh["poswx_wh_url"])

            # See about sending to a club system 
            if club_telegram: # Send Status to Telegram
                send_telegram(status, msg_type, lat,lng, telegramkeys["club_bot_token"], telegramkeys["club_chat_id"])

            if club_discord: # Send Status to Discord
                send_discord(status, discordwh["club_wh_url"], msg_type, station)

            if club_mattermost: # Send Status to Mattermost
                send_mattermost(status, mattermostwh["club_wh_url"], mattermostwh["club_apikey"])

            if club_slack: # Send Status to Slack
                slack_msg = {'text': slack_status}
                send_slack(slack_msg, slackwh["club_wh_url"])
        else: 
            print(status) # Send to Screen (for debugging)

###########################################
# Now Check for messages to my callsign(s) 

if aprsmsg_notify_telegram or aprsmsg_notify_discord or aprsmsg_notify_mattermost or aprsmsg_notify_slack or aprsmsg_notify_pushover:

    data = get_api_data_payload(aprsfi_api_base_url,msg_payload)

    x=0
    while x <= len(msg_callsign_list)-1 and x < data['found']:
        if int(data['entries'][x]["messageid"]) > lastmsgid:
            srccall = data['entries'][x]["srccall"]
            dstcall = data['entries'][x]["dst"]
            msg = data['entries'][x]["message"]
            dtstamp = data['entries'][x]["time"]
            lastmsgid = data['entries'][x]["messageid"]
            goodmsgdata = True
            break
        else:
            x=x+1
            goodmsgdata = False

    if goodmsgdata: # If we have good msg data
        msg_timestamp = datetime.datetime.fromtimestamp(int(dtstamp)).strftime('%H:%M:%S')
        msg_datestamp = datetime.datetime.fromtimestamp(int(dtstamp)).strftime('%m/%d/%Y')

        # create msg status and send to Telegram
        msg_status = "On " + msg_datestamp + " at " + msg_timestamp + ", " + srccall + " sent " + dstcall + " the following APRS message: " + msg

        msg_type = 3 # APRS Message Notification

        if not debug:
            if aprsmsg_notify_telegram:
                send_telegram(msg_status, msg_type, lat,lng, telegramkeys["my_bot_token"], telegramkeys["msg_chat_id"])
            if aprsmsg_notify_discord:
                send_discord(msg_status,discordwh["aprsmsg_wh_url"], msg_type,'')
            if aprsmsg_notify_pushover:
                send_pushover(msg_status)
            if aprsmsg_notify_slack:
                slack_msg = {'text': msg_status}
                send_slack(slack_msg,slackwh["aprsmsg_wh_url"])    
            if aprsmsg_notify_mattermost:
                send_mattermost(msg, mattermostwh["msg_wh_url"], mattermostwh["msg_apikey"])         
        else:
            print(msg_status) # Send to Screen (for debugging)

# Update aprsstamps table in database with lastmsgid/DT Stamp and close
sql = "update aprsstamps set lastpostime = " + str(lasttime) + ", lastmsgid = " + str(lastmsgid) + ", lastwxtime = " + str(lastwxtime) + ";"
if not debug:
    exec_sql(conn, sql)
else:
    print(sql)