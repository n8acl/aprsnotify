#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Current Version: 3.0
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@protonmail.com
# Twitter: @n8acl
# Telegram: @Ravendos
# Website: https://n8acl.ddns.net

#################################################################################
# Changes notes for next release. Basically reminder of changes done and when:
#################################################################################

###################   DO NOT CHANGE BELOW   #########################

# Import our Libraries and Configured variables

import config
import time
import os
import datetime
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
    import pickle
except ImportError:
    exit('This script requires the pickle module\nInstall with: pip3 install pickle')
try:
    from geopy.geocoders import Nominatim
except ImportError:
    exit('This script requires the geopy module\nInstall with: pip3 install geopy')
from time import sleep
from os import system

# Set Static Variables
version = '2.0'
degree_sign= u'\N{DEGREE SIGN}'
calllistlen = len(config.callsign_list)
fixed_station = 0
aprsfi_url = "https://api.aprs.fi/api/get"
owm_base_url = "http://api.openweathermap.org/data/2.5/weather"
geolocator = Nominatim(user_agent="aprstweet")
locdtstampfile = os.path.dirname(os.path.abspath(__file__)) + "/locdtstamp.txt"
srccall = "N0CALL"
msg = "No Message"

# Twitter API Object Configuration
auth = OAuthHandler(config.twitterkeys["consumer_key"], config.twitterkeys["consumer_secret"])
auth.set_access_token(config.twitterkeys["access_token"], config.twitterkeys["access_secret"])
twitter_api = tweepy.API(auth)

# Telegram bot configuration
bot = telegram.Bot(token=config.telegramkeys["my_bot_token"])

def get_json_payload(url,payload):
    # get json data from api's depending on the URL sent
    return requests.get(url=url,params=payload)

def get_curr_wx(owm_base_url, lat, lon):
    # Return Conditions and Temp for the packet location
    if config.units_to_use == 1:
        units = 'metric'
    else:
        units = 'imperial'

    payload = {
        'lat': lat,
        'lon': lon,
        'units': units,
        'appid': config.openweathermapkey
    }
    
    data = get_json_payload(owm_base_url,payload)
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

def send_status(msg,lat,lng):
    if (config.send_status_to == 0 or config.send_status_to == 1): # Send Status to Twitter
        twitter_status = msg + " #APRS"
        twitter_api.update_status(twitter_status)
    if (config.send_status_to == 0 or config.send_status_to == 2): # Send Status to Telegram
        tele_bot_message(msg)
        if (config.include_map_image == 1 or config.include_map_image == 3): # Includes a map of the packet location in Telegram
            bot.sendLocation(chat_id=config.telegramkeys["my_chat_id"], latitude=lat, longitude=lng, disable_notification=True)

def tele_bot_message(msg):
    # Sends the status message text to Telegram
    bot.sendMessage(chat_id=config.telegramkeys["my_chat_id"], text=msg)

# Main Program

# Check for locdtstamp.txt and create if does not exist
if not os.path.exists(locdtstampfile):
    with open(locdtstampfile,"wb") as f:
        chks = {"lasttime":"1","lastmsgid":"1"}
        pickle.dump(chks,f)
        f.close()

# Get packet time and last msg id from locdtstamp.txt
with open(locdtstampfile,"rb") as f:
    chks = pickle.load(f)
    f.close()

# get APRS Position Payload Information and store information in variables

position_payload = {
    'name': ",".join(config.callsign_list),
    'what': 'loc',
    'apikey': config.aprsfikey,
    'format': 'json'
}

data = get_json_payload(aprsfi_url,position_payload)

x=0
while x <= calllistlen-1 and x < data.json().get('found'):
    if int(data.json().get('entries')[x]["lasttime"]) > int(chks["lasttime"]):
        station = data.json().get('entries')[x]["name"]
        lat = data.json().get('entries')[x]["lat"]
        lng = data.json().get('entries')[x]["lng"]
        lasttime = data.json().get('entries')[x]["lasttime"]
        if "speed" in data.json().get('entries')[x]:
            speedkph = float(data.json().get('entries')[x]["speed"])
        else:
            fixed_station = 1
       
        gooddata = 1
        break
    else:
        x=x+1
        gooddata = 0

if gooddata == 1: # If we have a good set of packet data
    
    # Format Packet Time and Speed Data
    packet_timestamp = datetime.datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S')
    if fixed_station == 0:
        if config.units_to_use == 1:
            speed = speedkph
        else:
            speed = round(speedkph/1.609344,1)

    #Create Status Message
    status = station + ": "+ get_location(lat,lng)
        
    if fixed_station == 0:
        if config.units_to_use == 1:
            status = status + " | Speed: "+ str(speed) + " kph"
        else:
            status = status + " | Speed: "+ str(speed) + " mph"  
        
    status = status + " | Grid: " + get_grid(float(lat),float(lng))
    
    if config.include_wx == 1:
        #Get Weather Information
        conditions, temp = get_curr_wx(owm_base_url, lat, lng)

        if config.units_to_use == 1:
            status = status + " | WX: "+ str(temp) + degree_sign + " C & " + conditions
        else:
            status = status + " | WX: "+ str(temp) + degree_sign + " F & " + conditions

    status = status + " | " + packet_timestamp + \
        " | https://aprs.fi/" + station
    
    # Send packet Status
    # print(status) # Send to Screen (for debugging)
    send_status(status,lat,lng) # Send status to Social Networks
    
    chks["lasttime"] = lasttime

# Check for messages to my callsign(s) 
if config.enable_aprs_msg_notify == 1:
    msg_payload = {
        'what': 'msg',
        'dst': ",".join(config.callsign_list),
        'apikey': config.aprsfikey,
        'format': 'json'
    }

    data = get_json_payload(aprsfi_url,msg_payload)

    x=0
    while x <= calllistlen-1 and x < data.json().get('found'):
        if int(data.json().get('entries')[x]["messageid"]) > int(chks["lastmsgid"]):
            srccall = data.json().get('entries')[x]["srccall"]
            msg = data.json().get('entries')[x]["message"]
            lastmsgid = data.json().get('entries')[x]["messageid"]
            gooddata = 1
            break
        else:
            x=x+1
            gooddata = 0

    if gooddata == 1: # If we have good msg data
        # create msg status and send to Telegram
        msg_status = srccall + " sent you the following message on APRS: " + msg
        tele_bot_message(msg_status)

        chks["lastmsgid"] = lastmsgid

# Update locdtstamp.txt with lastmsgid/DT Stamp and close
with open(locdtstampfile,"wb") as f:
    pickle.dump(chks,f)
    f.close()
