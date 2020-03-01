# Make sure the following libraries have been installed with pip
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
from time import sleep
from tweepy import OAuthHandler
from geopy.geocoders import Nominatim

# Set Static Variables
degree_sign= u'\N{DEGREE SIGN}'
calllistlen = len(config.callsign_list)
current_time = time.strftime("%H:%M:%S")
aprsurl = "https://api.aprs.fi/api/get?name="+",".join(config.callsign_list) + "&what=loc&apikey=" + config.aprsfikey + "&format=json"
owm_base_url = "http://api.openweathermap.org/data/2.5/weather?"
geolocator = Nominatim(user_agent="aprstweet")
locdtstampfile = os.path.dirname(os.path.abspath(__file__)) + "/locdtstamp.txt"
setupfile = os.path.dirname(os.path.abspath(__file__)) + "/setup.py"

# Twitter API Object Configuration
auth = OAuthHandler(config.twitterkeys["consumer_key"], config.twitterkeys["consumer_secret"])
auth.set_access_token(config.twitterkeys["access_token"], config.twitterkeys["access_secret"])

twitter_api = tweepy.API(auth)

# Define Functions
def get_curr_wx(owm_base_url, lat, lon):
    # Return Conditions and Temp for the location
    wx_url = owm_base_url + "lat=" + lat + "&lon=" + lng + "&units=imperial&APPID=" + config.openweathermapkey
    with urllib.request.urlopen(wx_url) as url:
        data = json.loads(url.read().decode())
    return data["weather"][0]["main"], data["main"]["temp"] # Conditions, temp

def get_location(lat,lng):
    # Reverse geocode with google or openstreetmaps for location

    if config.geocoder_to_use == 1:
        with urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng='+ lat +','+lng +'&key=' + config.googlegeocodeapikey + '&sensor=false') as url:
            data = json.loads(url.read().decode())
        return data["results"][0]["formatted_address"]
    else:
        osm_address = geolocator.reverse(lat.strip()+","+lng.strip())
        return osm_address.address

def get_grid(dec_lat, dec_lon):
    ## Function developed by Walter Underwood, K6WRU https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square

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

def send_status(msg):
    if (config.send_status_to == 0 or config.send_status_to == 1): # Send Status to Twitter
        twitter_status = msg + " #APRS"   
        twitter_api.update_status(twitter_status) 

    if (config.send_status_to == 0 or config.send_status_to == 2): # Send Status to Telegram
        bot = telegram.Bot(token=config.telegramkeys["my_bot_token"])
        bot.sendMessage(chat_id=config.telegramkeys["my_chat_id"], text=msg)

# Main Program

# Check for locdtstamp.txt and create if does not exist
if not os.path.exists(locdtstampfile):
    with open(locdtstampfile,"w+") as f:
        f.write('1')
        f.close()

#Get Stored last time for time comparison
with open(locdtstampfile,"r") as f:
    filetime = int(f.read())
    f.close()

# get APRS Information and store information in variables
with urllib.request.urlopen(aprsurl) as url:
    data = json.loads(url.read().decode())

x=0
while x <= calllistlen-1 and x < data["found"]:
    if int(data["entries"][x]["lasttime"]) > filetime:
        station = data["entries"][x]["name"]
        lat = data["entries"][x]["lat"]
        lng = data["entries"][x]["lng"]
        lasttime = data["entries"][x]["lasttime"]
        speedkph = data["entries"][x]["speed"]
        gooddata = 1
        break
    else:
        x=x+1
        gooddata = 0

if gooddata == 1: # If we have a good set of packet data
    
    #Get Weather Information
    conditions, temp = get_curr_wx(owm_base_url, lat, lng)

    # Format Packet Time and Speed Data
    packet_timestamp = datetime.datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S')
    speedmph = round(speedkph/1.609344,1)

    #Create Status Message
    status = station + ": "+ get_location(lat,lng) + \
        " | Speed: "+ str(speedmph) + " mph "  + \
        " | Grid: " + get_grid(float(lat),float(lng)) + \
        " | WX: "+ str(temp) + degree_sign + " & " + conditions + \
        " | " + packet_timestamp + \
        " | https://aprs.fi/" + station
    
    # Send Status
    print(status) # Send to Screen (for debugging)
    send_status(status) # Send status to Social Networks
    
    # Update locdtstamp file with DT Stamp and close
    with open(locdtstampfile,"w+") as f:
        f.write(lasttime)
        f.close()
        
