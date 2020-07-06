#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Inital Release Date: 02/22/2020
# Current Release Date: 07/06/2020
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@protonmail.com
# Twitter: @n8acl
# Telegram: @Ravendos
# Website: https://n8acl.ddns.net

#################################################################################

# Make sure the following libraries have been installed with pip3
# pip3 install python-telegram-bot --upgrade
# pip3 install Tweepy
# pip3 install geopy

###################   DO NOT CHANGE BELOW   #########################

# Import our Libraries and Configured variables

import config
import telegram
import tweepy
import time
import urllib.request, json
import os
import datetime
import pickle
from time import sleep
from tweepy import OAuthHandler
from geopy.geocoders import Nominatim
from os import system

# Set Static Variables
version = '2.0'
degree_sign= u'\N{DEGREE SIGN}'
calllistlen = len(config.callsign_list)
fixed_station = 0
aprsurl = "https://api.aprs.fi/api/get?name="+",".join(config.callsign_list) + "&what=loc&apikey=" + config.aprsfikey + "&format=json"
msgurl = "https://api.aprs.fi/api/get?what=msg&dst="+",".join(config.callsign_list) + "&apikey=" + config.aprsfikey + "&format=json"
owm_base_url = "http://api.openweathermap.org/data/2.5/weather?"
googlegeocode_baseurl = "https://maps.googleapis.com/maps/api/geocode/json?"
geolocator = Nominatim(user_agent="aprstweet")
locdtstampfile = os.path.dirname(os.path.abspath(__file__)) + "/locdtstamp.txt"
updatefile = os.path.dirname(os.path.abspath(__file__)) + "/update.py"
filedellist = ['update.py','config_old.py']

# Twitter API Object Configuration
auth = OAuthHandler(config.twitterkeys["consumer_key"], config.twitterkeys["consumer_secret"])
auth.set_access_token(config.twitterkeys["access_token"], config.twitterkeys["access_secret"])
twitter_api = tweepy.API(auth)

# Telegram bot configuration
bot = telegram.Bot(token=config.telegramkeys["my_bot_token"])

# Define Functions
def check_version(version):
    if config.version == version:
        if name == 'nt': # windows
            for x in filedellist:
                cmd = "del " + x
                os.system(cmd)
        else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
            for x in filedellist:
                cmd = "rm " + x
                os.system(cmd)

def get_json_payload(url):
    # get json data from api's depending on the URL sent
    with urllib.request.urlopen(url) as url:
        return json.loads(url.read().decode())

def get_curr_wx(owm_base_url, lat, lon):
    # Return Conditions and Temp for the packet location
    if config.units_to_use == 1:
        wx_url = owm_base_url + "lat=" + lat + "&lon=" + lng + "&units=metric&APPID=" + config.openweathermapkey
    else:
        wx_url = owm_base_url + "lat=" + lat + "&lon=" + lng + "&units=imperial&APPID=" + config.openweathermapkey

    data = get_json_payload(wx_url)

    return data["weather"][0]["main"], data["main"]["temp"] # Conditions, temp

def get_location(lat,lng):
    # Reverse geocode with google or openstreetmaps for location

    if config.geocoder_to_use == 1:
        googlegeocodeurl = googlegeocode_baseurl + 'latlng='+ lat +','+lng +'&key=' + config.googlegeocodeapikey + '&sensor=false'
        data = get_json_payload(googlegeocodeurl)
        return data["results"][0]["formatted_address"]
    else:
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

# Check to see if update.py exists and then check the version and delete if the version of the config file
# and version of the main script are the same. This should indicate that the update.py has already been run
# and the config file updated.
# if os.path.exists(updatefile):
#     check_version(version)

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

# get APRS Payload Information and store information in variables
data = get_json_payload(aprsurl)

x=0
while x <= calllistlen-1 and x < data["found"]:
    if int(data["entries"][x]["lasttime"]) > int(chks["lasttime"]):
        station = data["entries"][x]["name"]
        lat = data["entries"][x]["lat"]
        lng = data["entries"][x]["lng"]
        lasttime = data["entries"][x]["lasttime"]
        if "speed" in data["entries"][x]:
            speedkph = float(data["entries"][x]["speed"])
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

# Check for messages to my callsign 
if config.enable_aprs_msg_notify == 1:
    data = get_json_payload(msgurl)

    x=0
    while x <= calllistlen-1 and x < data["found"]:
        if int(data["entries"][x]["messageid"]) > int(chks["lastmsgid"]):
            srccall = data["entries"][x]["srccall"]
            msg = data["entries"][x]["message"]
            lastmsgid = data["entries"][x]["messageid"]
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
