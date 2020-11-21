#################################################################################

# APRSNotify APRS Interactive Bot
# Developed by: Jeff Lehman, N8ACL
# Current Version: 1.0
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@protonmail.com
# Twitter: @n8acl
# Telegram: @Ravendos
# Website: https://n8acl.ddns.net
#################################################################################

import telebot
import threading
import time
import os
import datetime
import requests
import aprslib
import config
from geopy.geocoders import Nominatim
from aprslib.util import latitude_to_ddm, longitude_to_ddm 
from time import sleep
from os import system

##### Define Variables
# Misc Variables
degree_sign= u'\N{DEGREE SIGN}'
linefeed = "\r\n"
startup = 0
# URL/File Variables
aprsfi_url = "https://api.aprs.fi/api/get"
owm_base_url = "http://api.openweathermap.org/data/2.5/weather"
# APRS-IS Variables
port = 14580
passcode = aprslib.passcode(config.aprsbot_callsign)
icon = "/$" # First character is the table index and second is the table code. Some lists show this reversed (code first and then table index).
# Telebot Variables
BOT_TOKEN = config.telegramkeys["my_bot_token"]
BOT_INTERVAL = 3
BOT_TIMEOUT = 30
bot = None
## Configure Objects
geolocator = Nominatim(user_agent="aprstweet")
AIS = aprslib.IS(config.aprsbot_callsign, passwd = passcode, port=port)
AIS.connect() # APRS-IS Connection Opened

## Define Functions
def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions() #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop

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
    osm_address = geolocator.reverse(str(lat).strip()+","+str(lng).strip())
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

# searches and returns APRS postion packet for station
def find_aprs_station(callsign):
    fixed_station=0

    position_payload = {
    'name': ",".join(callsign),
    'what': 'loc',
    'apikey': config.aprsfikey,
    'format': 'json'
    }

    data = get_json_payload(aprsfi_url,position_payload)
   
    if data.json().get('found') == 0:
        return "No data found for callsign %s." % "".join(callsign).upper()

    else:
        x=0    
        station = data.json().get('entries')[x]["name"]
        lat = data.json().get('entries')[x]["lat"]
        lng = data.json().get('entries')[x]["lng"]
        lasttime = data.json().get('entries')[x]["lasttime"]
        if "speed" in data.json().get('entries')[x]:
            speedkph = float(data.json().get('entries')[x]["speed"])
        else:
            fixed_station = 1

        #format packet timestamp
        packet_timestamp = datetime.datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S')

        #Create Status Message
        status = station + ": "+ get_location(lat,lng)

        if fixed_station == 0:
            if config.units_to_use == 1:
                status = status + " | Speed: "+ str(speedkph) + " kph"
            else:
                status = status + " | Speed: "+ str(round(speedkph/1.609344,1)) + " mph"  

        status = status + " | Grid: " + get_grid(float(lat),float(lng))

        #Get Weather Information
        conditions, temp = get_curr_wx(owm_base_url, lat, lng)
        if config.units_to_use == 1:
            status = status + " | WX: "+ str(temp) + degree_sign + " C & " + conditions
        else:
            status = status + " | WX: "+ str(temp) + degree_sign + " F & " + conditions
        status = status + " | " + packet_timestamp + " | https://aprs.fi/" + station
        return status, lat, lng

# Send postion to APRS-IS
def send_position(lat,lon):
    beacon_text = config.aprsbot_callsign + ">APN100,TCPIP*:="+ aprslib.util.latitude_to_ddm(lat) + icon[0:1] + aprslib.util.longitude_to_ddm(lon) + icon[1:2] + "Jeff, N8ACL | Mobile on Phone from Telegram" # Object Beacon
    AIS.sendall(beacon_text)

# Send Message to APRS-IS
def send_aprs_message(text):
    dst_callsign = ''.join(text.split()[1:2]).upper()
    msg_txt = ' '.join((text.split()[2 : len( text)]))

    while len(dst_callsign)<9:
        dst_callsign = dst_callsign + ' '

    aprs_msg = config.aprsbot_callsign + ">APN100,TCPIP*::" + dst_callsign + ':' + msg_txt
    AIS.sendall(aprs_msg)

# Extract arguments
def extract_args(arg):
    return arg.split()[1:]

# One place to send messages from
def bot_send_message(txt):
    if txt != '':
        bot.send_message(config.telegramkeys["my_chat_id"],txt)

# Send mapped location on /find
def bot_send_location(lat,lon):
    bot.send_location(config.telegramkeys["my_chat_id"], lat, lon)

def botactions():
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Hi there, I am APRSBot.
    I am here to let you interact with the APRS Network from Telegram!\
    """)
    # Handle '/help' 
    @bot.message_handler(commands=['help'])
    def send_help(message):
        help_txt = "Hello I am APRSBot, Companion app to APRSNotify. I am here to allow you to interact with the APRS Network from Telegram." + linefeed + linefeed + \
            "Available Commands: " + linefeed + \
            "/help - This help list" + linefeed + \
            "/find <callsign> - Pull last position for a station. <callsign> is either callsign or callsign-ssid (Example: AA0ABC or AA0ABC-9)" + linefeed + \
            "/msg <callsign> <message text> - Send a message to an APRS Station. <callsign> is the destination callsign and is either callsign or callsign-ssid (Example: AA0ABC or AA0ABC-9) and message text is the message you want to send to." + linefeed + \
            "To send current location, click the paperclip, select location and then select send current location. You will get a map image showing your current location and it will be sent to the APRS-IS System"
        bot_send_message(help_txt)

    # Handle '/find'
    @bot.message_handler(commands=['find'])
    def handle_callsign_search(message):
        bot_send_message('One Moment while I retrieve that for you.....')
        status, lat, lon = find_aprs_station(extract_args(message.text))
        bot_send_message(status)
        bot_send_location(lat,lon)

    # Handle '/ping'
    @bot.message_handler(commands=['ping'])
    def handle_callsign_search(message):
        bot_send_message('pong')    

    # Handle '/msg'
    @bot.message_handler(commands=['msg'])
    def handle_callsign_search(message):
        bot_send_message('Message Received.... Relaying to the APRS-IS network')    
        send_aprs_message(message.text)

    # Handle Location
    @bot.message_handler(content_types=['location'])
    def handle_location(message):
        #print("{0}, {1}".format(message.location.latitude, message.location.longitude))
        send_position(message.location.latitude,message.location.longitude)
        bot_send_message("Location Received.... Transmitting to the APRS-IS Network")

    # Handle all other messages with content_type 'text' (content_types defaults to ['text']) as Error messages
    @bot.message_handler(func=lambda message: True)
    def error_message(message):
        bot_send_message("I'm sorry I don't understand that.")

polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()

#Keep main program running while bot runs threaded
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break