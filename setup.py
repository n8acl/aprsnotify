# Setup script for APRSNotify

# Import libraries
import os
from os import system, name


# Define Static Variables
configfile = os.path.dirname(os.path.abspath(__file__)) + "/config.py"
linefeed = "\n"
linebreak = "------------------------------------------------------"
title_line = "APRSNotify First Run Configuration Utility"
send_status_to = -1
geocoder_to_use = -1

# Define Functions
def clear_screen(): # Defines function to clear the screen to make output easier to read
    if name == 'nt': # windows
        _ = system('cls')
    else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
        _ = system('clear')

def get_services(arg):
    
    switcher = {
        0: "All",
        1: "Twitter",
        2: "Telegram"
    }
    return switcher.get(arg,"Nothing")

def get_geocoder(arg):
    
    switcher = {
        1: "Google",
        2: "OpenStreetMaps"
    }
    return switcher.get(arg,"Nothing")


# Main Program
clear_screen() # Clears the screen to make output easier to read

msg = title_line + """

PLEASE READ THIS FIRST!

This utility will help you to configure the APRSNotify configuration file for this first run of the APRSNotify Script. 

Please follow the directions found in the README at https://github.com/n8acl/aprsnotify in order to obtain the 
API keys you will need for this script.

When this utility is finished, the setup.py file will be renamed to setup.txt to prevent running the script again accidently. If this utility
needs to be run again in the future, just rename the setup.txt file to setup.py and run APRSNotify again.

You can also edit the config.py file directly. Instructions are included in that file if edits need to be made.
""" + linefeed + linefeed

print(msg)

pause = input("When you are ready to continue, please press enter.")
#-----------------------------------------

clear_screen() # Clears the screen to make output easier to read

msg = title_line 

print(msg)

if os.path.exists(configfile):

    msg = """

    Previous config.py file was detected.""" + linefeed + linefeed
    print(msg)

    cpyfile = input("Would you like to copy this file to config.old for backup? (y/n)")
    if cpyfile == 'y':
        if name == 'nt': # windows
            cmd = "copy config.py config.old"
            os.system(cmd)
        else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
            cmd = "mv config.py config.old"
            os.system(cmd)
        msg = "Your config.py file has been renamed config.old"
    else:
        msg = "YOUR CONFIG.PY FILE HAS NOT BEEN BACKED UP. Note that this utility will overwrite the existing file."
    print(linefeed+linefeed+msg)

msg = ""

msg = msg + """

First we need to choose and configure the Social Media service(s) you plan to use. 
All sends to both Twitter and Telegram, or you can select one of the services to send to.

0 = All
1 = Twitter
2 = Telegram
"""
print(msg)

while (send_status_to != 1 or send_status_to !=2 or send_status != 0):
    send_status_to = int(input("Enter the number of the service(s) you want to use: "))
    if (send_status_to == 1 or send_status_to == 2 or send_status_to ==0):
        break

msg = linefeed + "You choose:" + linefeed + get_services(send_status_to) + linefeed

print(msg)

if (send_status_to == 0 or send_status_to == 1):
    msg = "In order to use Twitter, You will need to obtain 4 API Keys from them: consumer_key, consumer_secret, access_token, access_secret " + linefeed + linefeed
    print(msg)
    consumer_key = input("Please copy and paste your consumer_key here: ")
    consumer_secret = input("Please copy and paste your consumer_secret here: ")
    access_token = input("Please copy and paste your access_token here: ")
    access_secret = input("Please copy and paste your access_secret here: ")
    print(linefeed)
if (send_status_to == 0 or send_status_to == 2):
    msg = "In order to use Telegram, you will need to obtain 2 API Keys from them: Your Bot Token and your chatid " + linefeed + linefeed
    print(msg)
    my_bot_token = input("Please copy and paste your Bot Token here: ")
    my_chat_id = input("Please copy and paste your Chatid here: ")
    
#-----------------------------------------
clear_screen()

msg = title_line + """

Now we need to choose the Geocoding API you would like to use. 

1 = Google (API Key Needed)
2 = OpenStreetMaps (No API Key Needed)
"""
print(msg)

while (geocoder_to_use != 1 or geocoder_to_use !=2):
    geocoder_to_use = int(input("Please enter the number of the Geocoding API service to use: "))
    if (geocoder_to_use == 1 or geocoder_to_use ==2):
        break

msg = linefeed + "You choose:" + linefeed + get_geocoder(geocoder_to_use) + linefeed + linefeed

if geocoder_to_use == 1:
    msg = """In Order to use the Google Geocoding API, you will need to obtain an API key from Google.""" + linefeed + linefeed
    print(msg)
    googlegeocodeapikey = input("Please copy and paste the API from Google here: ")

#-----------------------------------------
clear_screen()

msg = title_line +"""

Now we have the last few things we need to configure for the script.
"""

print(msg)

callsignlist = list(map(str,input("Please enter the list of callsigns with ssid that you would like to track (ex: AA0ABC-1,AA0ABC-2,...): ").split(',')))
aprsfikey = input("Please copy and paste your APRS.FI API key here: ")
openweathermapkey = input("Please copy and paste your OpenWeatherMap API Key here: ")

#-----------------------------------------

txt = """#################################################################################

# APRSNotify
# Developed by: Jeff Lehman, N8ACL
# Inital Release Date: 02/22/2020
# https://github.com/n8acl/aprsnotify

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@protonmail.com
# Twitter: @n8acl
# Telegram: @Ravendos
# Website: https://n8acl.ddns.net

#################################################################################

# Make sure the following libraries have been installed with pip3 prior to starting this.
# pip3 install python-telegram-bot --upgrade
# pip3 install Tweepy --upgrade
# pip3 install geopy --upgrade

#################################################################################

## select which service to send the status to. Default is 0 (all):
# 0 = All
# 1 = Twitter
# 2 = Telegram
"""
txt = txt + "send_status_to = " + str(send_status_to)

txt = txt + """

## Select Geocoder to use. Default is 2 (OpenStreetMaps):
# 1 = Google
# 2 = OpenStreetMaps
"""

txt = txt + "geocoder_to_use = " + str(geocoder_to_use)

txt = txt + """

## Configure Twitter Keys
twitterkeys = {
    "consumer_key": """
if (send_status_to == 0 or send_status_to == 1):
    txt = txt + '"' + consumer_key + '",' + linefeed
    txt = txt + '    "consumer_secret": "' + consumer_secret + '",' + linefeed
    txt = txt + '    "access_token": "' + access_token + '",' + linefeed
    txt = txt + '    "access_secret": "' + access_secret + '"' + linefeed
else:
    txt = txt + '"YOUR CONSUMER KEY HERE",' + linefeed
    txt = txt + '    "consumer_secret": "YOUR CONSUMER SECRET KEY HERE",' + linefeed
    txt = txt + '    "access_token": "YOUR ACCESS TOKEN HERE",' + linefeed
    txt = txt + '    "access_secret": "YOUR ACCESS SECRET KEY HERE"' + linefeed
txt = txt + "}"

txt = txt + """

## Configure Telegram Keys

telegramkeys = {
    "my_bot_token": """

if (send_status_to == 0 or send_status_to == 2):
    txt = txt + '"' + my_bot_token + '",' + linefeed
    txt = txt + '    "my_chat_id": "' + my_chat_id + '"' + linefeed
else:
    txt = txt + '"YOUR BOT TOKEN HERE",' + linefeed
    txt = txt + '    "my_chat_id": "YOUR CHAT ID HERE"' + linefeed
txt = txt + "}"

txt = txt + """

## Configure Other API Keys and Variables
"""
txt = txt + 'callsign_list = ['

for i in range(0,len(callsignlist)):
    txt = txt + '"' + callsignlist[i].upper() + '"'
    if i != len(callsignlist)-1:
        txt = txt + ","

txt = txt + '] # This is the list of callsigns with ssid to monitor and tweet. You need at least one but can be as many as you want separated by commas' + linefeed

txt = txt + 'aprsfikey = "' + aprsfikey + '" # This is your API key from your APRS.fi account' + linefeed
if geocoder_to_use == 1:
    txt = txt + 'googlegeocodeapikey = "' + googlegeocodeapikey + '" # this is your Google Geocodeing API Key' + linefeed
else: 
    txt = txt + 'googlegeocodeapikey = "YOUR GOOGLE GEOCODING API KEY HERE" # this is your Google Geocodeing API Key' + linefeed

txt = txt + 'openweathermapkey = "' + openweathermapkey + '" # This is your OpenWeatherMap API Key.' + linefeed

with open(configfile,"w+") as f:
    f.write(txt)
    f.close()

#-----------------------------------------
clear_screen()

msg = title_line +"""

Your config.py file has been built. 

This utility will be saved as setup.txt. If you would like to use this utility in the future to change configs,
just rename the file from setup.txt to setup.py and rerun the APRSNotify script and this utility will run again. 

It will save your existing config.py file to config.old as a backup if you need to reference it.

"""

print(msg)

pause = input("When you are ready to finish this script and let the rest of the program run, please press enter.")