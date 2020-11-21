# Setup script for APRSNotify

# Import libraries
import os
from os import system, name


# Define Static Variables
config_fname = "test"
config_old = config_fname + ".old"
configfile = config_fname + ".py"
linefeed = "\n"
linebreak = "------------------------------------------------------"
title_line = "APRSNotify Configuration Setup Utility"
send_status_to = -1
units_to_use = -1
include_wx = -1
include_map_image = -1
enable_aprs_msg_notify = -1

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

# Main Program
clear_screen() # Clears the screen to make output easier to read

msg = title_line + """

PLEASE READ THIS FIRST!

This utility will help you to configure the APRSNotify configuration file for the APRSNotify Bot Script. 

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

msg = ""

if os.path.exists(configfile):
    msg = "Previous config.py file detected. Copying to config.old."
    print (msg)
    if name == 'nt': # windows
        cmd = "copy " + configfile + " " + config_old
    else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
        cmd = "mv " + configfile + " " + config_old
    os.system(cmd)

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

msg = linefeed + "You chose:" + linefeed + get_services(send_status_to) + linefeed

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

What type of units of measure do you want to use?

1 = Metric (Celcius, Kilometers Per Hour, Etc)
2 = Imperial (Farenheit, Miles Per Hour, Etc)
"""
print(msg)

while (units_to_use != 1 or units_to_use != 2):
    units_to_use = int(input("Enter the number for the units you want to use: "))
    if (units_to_use == 1 or units_to_use == 2):
        break

#-----------------------------------------
if (send_status_to == 0 or send_status_to == 2): 

    clear_screen()

    msg = title_line + """

Since you indicated earlier that you are using Telegram, you could use APRS message notification if you want.
If someone sends a messsage to one of the callsigns being tracked by this script, the script will send you a notification
on Telegram. You would also be able to send messages from Telegram to APRS as well if you are using the APRSBot companion script.

Do you want to enable or disable APRS message notification?

0 = Disable
1 = Enable
    """
    print(msg)

    while (enable_aprs_msg_notify != 1 or enable_aprs_msg_notify != 0):
        enable_aprs_msg_notify = int(input("Enter the number for you choice: "))
        if (enable_aprs_msg_notify == 1 or enable_aprs_msg_notify == 0):
            break   

    #-----------------------------------------
    clear_screen()

    msg = title_line + """

You can also include a map image on your Telegram posts.
Do you want to include a map image on your Telegram posts?

0 = No
1 = Yes
    """
    print(msg)

    while (include_map_image != 1 or include_map_image != 0):
        include_map_image = int(input("Enter the number for your choice: "))
        if (include_map_image == 1 or include_map_image == 0):
            break
else:
    enable_aprs_msg_notify = 0
    include_map_image = 0
#-----------------------------------------
clear_screen()

msg = title_line + """

Also, do you want to include a weather report in your status?
Note that this will require an API key from OpenWeatherMap at https://openweathermap.org/api to work. 

0 = Disable
1 = Enable
"""
print(msg)

while (include_wx != 1 or include_wx != 0):
    include_wx = int(input("Enter the number of your choice: "))
    if (include_wx == 1 or include_wx == 0):
        break

#-----------------------------------------
clear_screen()

msg = title_line +"""

Now we have the last few things we need to configure for the script.
"""

print(msg)

aprsbot_callsign = input("If you are going to use the interactive APRSBot companion script with Telegram, please enter a callsign for the bot to use with APRS-IS (ex: AA0ABC-1): ")
callsignlist = list(map(str,input("Please enter the list of callsigns with ssid that you would like to track seperated by commas (ex: AA0ABC-1,AA0ABC-2,...). You may want to include the Callsign for the bot from above too: ").split(',')))
aprsfikey = input("Please copy and paste your APRS.FI API key here: ")
if include_wx == 1:
    openweathermapkey = input("Please copy and paste your OpenWeatherMap API Key here: ")

#-----------------------------------------

txt = """###############################################
# Configuration File for APRSNotify and APRSBot
# Questions about this file, please go to:
# https://github.com/n8acl/aprsnotify/blob/master/configuration.md
###############################################

## select which service to send the status to. Default is 0 (all):
# 0 = All
# 1 = Twitter
# 2 = Telegram
"""
txt = txt + "send_status_to = " + str(send_status_to)

txt = txt + """

## Select Unit Type to use. Default is 2 (Imperial):
# 1 = Metric
# 2 = Imperial
"""
txt = txt + "units_to_use = " + str(units_to_use)

txt = txt + """

## Enable APRS Message notification. Default is 0 (No):
## Note: You must provide a Telegram Bot Key and Chat ID below for messaging notification to work.
# 0 = No
# 1 = Yes
"""

txt = txt + "enable_aprs_msg_notify = " + str(enable_aprs_msg_notify)

txt = txt + """

## Include Map image in status. Default is 0 (No):
## Note: You must provide a Telegram Bot Key and Chat ID below for messaging notification to work.
# 0 = No
# 1 = All -- for future use -- DO NOT USE YET
# 2 = Twitter Only -- for future use -- DO NOT USE YET
# 3 = Telegram Only
"""
txt = txt + "include_map_image = "

if include_map_image == 1:
    txt = txt + "3"
else:
    txt = txt + "0"

txt = txt + """

## Include Weather information in status. Default is 1 (Yes):
# 0 = No
# 1 = Yes
"""
txt = txt + "include_wx = " + str(include_wx)

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

txt = txt + 'aprsbot_callsign = "' + aprsbot_callsign + '" # This is the callsign that APRSBot will use to send your location and any messages from Telegram to the APRS-IS Network.' + linefeed

txt = txt + 'aprsfikey = "' + aprsfikey + '" # This is your API key from your APRS.fi account' + linefeed
if include_wx == 1:
    txt = txt + 'openweathermapkey = "' + openweathermapkey + '" # This is your OpenWeatherMap API Key.' + linefeed
else:
    txt = txt + 'openweathermapkey = "YOUR OPENWEATHERMAP API KEY HERE" # This is your OpenWeatherMap API Key.' + linefeed


with open(configfile,"w+") as f:
    f.write(txt)
    f.close()

#-----------------------------------------
clear_screen()

msg = title_line +"""

Your config.py file has been built. 

This utility will be saved as setup.txt. If you would like to use this utility in the future to change configs,
just rename the file from setup.txt to setup.py and rerun the APRSNotify script and this utility will run again. 

If you had an existing config file, it copied your existing config.py file to config.old as a backup if you need to reference it.

"""

print(msg)

pause = input("When you are ready to finish this script, please press enter.")