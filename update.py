import importlib
import os
from os import system, name

# Define Static Variables
old_version = 1.0
new_version = 2.0
configold = "config_old.py"
configfile = "config.py"
linefeed = "\n"
linebreak = "------------------------------------------------------"
title_line = "APRSNotify Configuration Update Utility"
units_to_use = -1
include_wx = -1
include_map_image = -1
enable_aprs_msg_notify = -1

if os.path.exists(configfile):
    if name == 'nt': # windows
        cmd = "copy " + configfile + " " + configold
    else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
        cmd = "cp " + configfile + " " + configold
    os.system(cmd)


    # Define Functions
    def clear_screen(): # Defines function to clear the screen to make output easier to read
        if name == 'nt': # windows
            _ = system('cls')
        else: # MacOS (The Second best operating system ever) and Linux (The best operating system ever)
            _ = system('clear')


    import config_old

    # Main Program

    clear_screen() # Clears the screen to make output easier to read

    msg = title_line + """

PLEASE READ THIS FIRST!

This utility will update your APRSNotify configuration file (config.py) from version """

    msg = msg + str(old_version) + " to version " + str(new_version)

    msg = msg + """.

When this utility is finished and APRSNotify next run, the update.py file will be deleted to prevent running 
the script again accidently. If updates to the config.py file need to be made in the future, just 
run the setup.py file. You can also edit the config.py file directly. Instructions are included in that file if edits need to be made.
    """ + linefeed + linefeed

    print(msg)

    pause = input("When you are ready to continue, please press enter.")
    #-----------------------------------------

    clear_screen() # Clears the screen to make output easier to read

    msg = title_line 

    print(msg)

    msg = """

We need to set the switches for the new features now....

First, what type of unit of measurement would you like to use?
1 = Metric (Celcius, Kilometers Per Hour, etc)
2 = Imperial (Farenheit, Miles Per Hour, etc)
    """

    print(msg)

    while (units_to_use != 1 or units_to_use !=2):
        units_to_use = int(input("Enter the number of units of measure you want to use: "))
        if (units_to_use == 1 or units_to_use == 2 ):
            break

    #-----------------------------
    if (config_old.send_status_to == 0) or (config_old.send_status_to == 2):
        clear_screen() # Clears the screen to make output easier to read

        msg = title_line 

        print(msg)

        msg = """

It looks like you are using Telegram and have a Telegram Bot setup.
Would you like to enable APRS Message Notifications? If someone sends a message to one of your callsigns
being tracked by the ARPSNotify Script, the script will send you a notification of that message to Telegram.

0 = Disable
1 = Enable
        """

        print(msg)

        while (enable_aprs_msg_notify != 1 or enable_aprs_msg_notify != 0):
            enable_aprs_msg_notify = int(input("Enter the number of your choice: "))
            if (enable_aprs_msg_notify == 1 or enable_aprs_msg_notify == 0):
                break
        
        #-------------------------------------

        clear_screen() # Clears the screen to make output easier to read

        msg = title_line 

        print(msg)

        msg = """
    
Since you are using Telegram, you could also include a map image with your location to Telegram. Would you
like to do that?
0 = No
1 = Yes
        """

        print(msg)

        while (include_map_image != 1 or include_map_image != 0):
            include_map_image = int(input("Enter the number of your choice: "))
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

    #------------------------------------------


    txt = """

#------------------------------------------
BELOW ADDED WITH UPDATE FROM VERSION """

    txt = txt + old_version

    txt = txt + " TO VERSION " + new_version

    txt = txt + """

## Current Version
version = 2.0

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

    with open(configfile,"a") as f:
        f.write(txt)
        f.close()    

    #-----------------------------------------
    clear_screen()

    msg = title_line +"""

Your config.py file has been updated. 

    """
else:

    clear_screen()

    msg = title_line +"""

You do not have an existing config.py file. Please run setup.py to setup the configuration file. 

    """

print(msg)
pause = input("When you are ready to finish this script, please press enter.")