# APRSNotify
APRSNotify is a python based bot script designed to send parsed APRS packet data to Twitter and/or Telegram. This bot has both an interactive part and a notifier part to it. The interactive part of the bot only works with Telegram.

This software is for use by Amatuer Radio Operators only.

---

## Table of Contents
- [Features](https://github.com/n8acl/aprsnotify#Features)
- [Description](https://github.com/n8acl/aprsnotify#Description)
- [Installation](https://github.com/n8acl/aprsnotify#Installation/Setup)
- [Running the Script](https://github.com/n8acl/aprsnotify#Runningthescript)
- [Interacting with the Bot on Telegram](https://github.com/n8acl/aprsnotify/blob/master/botcommands.md)
- [Credits](https://github.com/n8acl/aprsnotify#credits)
- [Contact Me](https://github.com/n8acl/aprsnotify#contact)
- [Change Log](https://github.com/n8acl/aprsnotify#changelog)

---

## Features
- Setup Utility for creating your config file.
- Pull most recent packet data from [APRS.fi API](https://aprs.fi/page/api).
- Reverse Geocode with OpenStreetMaps API.
- Get Weather Information from OpenWeatherMaps API for the location of the packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (currently Twitter and Telegram)
- Get notification of an APRS message sent to your station (requires Telegram to work). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and show you the message on Telegram. You can then send a response to the message from Telegram.
- Retrieve a stations last packet and send your location without a radio (requires Telegram to work).
- Send a message to an APRS Station from Telegram.

---
## UPDATING TO RELEASE 3.1

If you are running an older version of APRSnotify, you will need to run the setup.py utility again after cloning everything here. Make sure to backup your config.py file before cloning. 

There are a couple new variables, so you will need to rebuild the config file when updating this release. You can use your old config.py file to reference your api keys. That is why you need to make sure to back it up somewhere you can access it. You will need to edit the file and copy out your keys to enter into the new config file while working through the setup.py utility.

---

## Description
This script is made up of two parts that can be used together or seperatly, depending on the users wants/needs.

APRSNotify: This is the main part of the script and the notification portion if it. This script will pull your most recent APRS packet data from the [APRS.fi API](https://aprs.fi/page/api), will parse the data and send the data to various social media accounts (currently either a Twitter account and/or to Telegram via a Telegram Bot). The script will only pull your most recent packet and post it once. 

APRSBot: The second part of the script is an interactive bot that works with Telegram. This part of the bot will allow the user to pull any station packet and show it as well as send your location to the APRS-IS system, allowing you to send your location from your phone to the APRS network and be seen on sites like APRS.fi and APRSDirect. If you set up the Callsign-ssid as part of the APRSNotify tracking list, it will also send that packet to Twitter and Telegram for you.

This script can also notify you, via Telegram, if someone/something sends you a message on APRS. This way you can stay on top and see if there are messages being sent to you by another station. This is useful for monitoring a remote station. If something trips, a message could be sent via APRS to someone and then they know that something has happened at the remote site.

In regards to Telegram bots, again, depending on your what/needs, if you are just going to use the notifier portion and you have an existing bot that you would like to use, that would be fine. However, if you would like to use the interactive portion of the bot, I would recommend creating a seperate APRS bot to be used for both the notifier and the interactive bot. This will keep everyting together and since both parts of the package pull from the same config file, it makes it easier.

Note that this bot package was designed to be used by one person with multiple APRS Trackers to track packets from that one person.

If you would like to see a working example, at least on Twitter of what the notifier portion does, please check out [@n8acl_aprs](https://twitter.com/n8acl_aprs) on Twitter.

This script does take a little bit to get configured to run, the biggest portion of it being getting all the API keys that you will need for the script, but once those are in place, the script is very easy to run, just set it and forget it.

The scripts can be run from a cronjob (Linux) or Task Scheduler (Windows) and is lightweight enough to even be run on a Raspberry Pi Zero W.

Most of the instructions in this README assume that you are using Linux to setup your script to run. If you want to run it on Windows or Mac, you will need to install Python based on instructions for those OS's and know how to setup Task Scheduler, but the configuration of the script itself is the same.

### Use Cases
* Sending an APRS packet to Twitter for your followers to see.
* Sending APRS data to yourself to confirm that it is making it to the internet (via Telegram for example).
* Sending your position information to a Telegram Channel that you have your non-ham radio family and friends on so they can track you when you are traveling by car for a long distance.
* Sending position data to a radio club Telegram Channel so that everyone can see your data posted.
* Other uses that your imagination comes up with.

---

# Installation/Setup
To install the script, please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/n8acl/aprsnotify.git

cd /aprsnotify

pip3 install -r requirements.txt

chmod +x startbot.sh
```

### API Keys Needed
Because of the nature of the API's being used, you will need to get your own API keys from the following:

* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need. Without this, nothing else will work.
    - NOTE: There is a limit to the API. You can use 20 callsigns to find the positions of and 10 to pull messages for. 

* [OpenWeatherMap](https://openweathermap.org/api) to pull your weather data based on packet location data. This is a free account, but you are limited to 60 calls per minute and 1000 calls per day. You do need this for the script to work.

* If you plan on using Telegram:
    - You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
    - You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
    - Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
    - NOTE: Telegram is required for APRS message notification and for the interactive part of the bot to work.

* If you plan on using Twitter:
    - You will need to get a consumer key, consumer secret, access token and access secret for the account you are wanting to post to. You can get those keys from The Twitter development site. Here is a walk through how: [Generate Twitter API Keys](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/)

### Configure the Script
Once you have your API Keys, you can now start configuring your APRSNotify bot. To start the process, in the directory where you have the APRSNotify bot files you just downloaded/cloned, enter the command:
```bash
python3 setup.py
```
This will start the setup utility. The setup utility will walk you through the process of configuring the various needed variables and ask you for your API Keys. 

You can also edit the config.py file directly in a text/python editor if you wish after it has been created. If you need a walkthrough of the configuration file for future editing, please [click here](https://github.com/n8acl/aprsnotify/blob/master/configuration.md#configuration-file-walkthrough).

---

## Running the Script
Once you have walked through the setup utility, you can run the script for a test. To run the script, you can use the command
```bash
python3 aprsnotify.py
```
in the directory where you have the script's files. When you run this manually, you will see the latest packet you sent displayed to the screen and if you look at Telegram/Twitter, you will see it there as well. This let's you know that you have everything configured correctly and everything is working fine.

Once you have confirmed that the script is running and everything is working, you can now setup to run the script automatically either via Task Scheduler in Windows or by adding a cronjob on Linux.

Edit your crontab file:

```bash
crontab -e
```

and then add the following lines to your crontab:

```bash
*/10 * * * * python3 aprsnotify/aprsnotify.py
@reboot aprsnotify/startbot.sh
```
In this example, the script runs every 10 minutes and will start the interactive telegram bot on reboot of the system. My APRS beacons are sent every 5 minutes from the car, so it will post approximately every other beacon. 

If you are not using the interactive bot, you can skip adding the @reboot line. All that does is start the bot on a reboot of the system.

If, for some reason, you need to access the bot script, to stop it or look for errors, you can use the following command to reattach to the session the bot is running in and control it from there:

```bash
screen -R aprsbot
```

Commands and other information about the bot can be found on the "Interacting with the Bot on Telegram" page.

---

## Credits
The Original Telegram Notify bot functionality was based off a gist by Github user Lucaspg96. [Click Here](https://gist.github.com/lucaspg96/284c9dbe01d05d0563fde8fbb00db220).

The Interactive APRSBot is based on a gist by Github user David-Lor [Click Here](https://gist.github.com/David-Lor/37e0ae02cd7fb1cd01085b2de553dde4)

The Grid Square Function was developed by Walter Underwood, K6WRU and posted on ham.stackexchange.com. [Click Here](https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square)

The map image functionality for the Telegram Bot and suggestions to include or not include Weather data amoung other suggestions were contributed by Chanyeol Yoo, Ph.D., VK2FAED

APRS.FI API Limitations issues found and troubleshot by [Alex Bowman, KN4KNG](https://github.com/KN4KNG). 

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Telegram: @ravendos
- E-mail: n8acl@protonmail.com

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log
* 12/11/2020 - Release 3.1 - Fixes around APRS.FI API limitations
    - APRSnotify
      - Updated aprsnotify.py to split position tracking and messge monitoring lists out to 2 seperate lists due to APRS.fi API restrictions
    - APRSbot
      - Updated aprsbot to fix APRS-IS Timeouts for sending locations and messages
    - README.md
      - Added limitations to the API to the APRS.fi API key section.
      - Other updates and clearifications to README.md
    - Configuration.md
      - Split callsign lists out to position tracking list and message list. This is due to limitations on the APRS.fi API

* 12/09/2020 - Minor update
    - Fixed Bug: fixed error in setup.py. Named the config file wrong in variable. (Found by [Alex Bowman, KN4KNG](https://github.com/KN4KNG))

* 11/15/2020 - Version 3.0 Release
    - Added/New Features:
        - Added a requirements.txt file to make installing libraries easier for end users
        - Added checks to make sure all python libraries needed are installed already and notify the user if not and how to install
        - Created and added new interactive bot functionality, APRSBot
    - Updates/Changes:
        - Changed from urllib to requests library to parse json. This makes it easier to use the same url for different purposes
        - Removed the aprs and msg url variables and combined into aprsfi_url variable for use with new library
        - Fixed bug: added srccall variable instantiation. This fixes a bug where if the srccall is not pulled properly the script bombs
        - Removed using Google Geocoder for Reverse geocoding. Only using OpenStreetMaps now
        - Updated README.md and Configuration.md files

* 08/20/2020
    - Updates to the ReadMe file

* 07/06/2020 - Version 2.0 Release
    - Added/New Features:
        - Ability to choose between Metric and Imperial units
        - Ability to turn off WX Information and not include it in the status message.
        - Now sends notification if someone sends the user a message on APRS (requires Telegram bot for this to work).
        - Sends map image of the packet location to Telegram (requires Telegram bot for this to work).
    - Updates:
        - Fixed: If there is not a speed entry in the JSON payload from APRS.FI, the script assumes it's a fixed station and does not include speed in the status message. In Ver. 1.0 this was a bug that would cause the script to fail if there was not a speed entry in the JSON payload.
        - Updated the config file to include switches for new features.
        - Updated the configuration walkthrough in this repo.
        - Updated Setup.py to include switches for new features. Will also update an existing config.py file to the new version. 
            - NOTE: If you are running version 1, when updating to Version 2 of the script, make sure to run setup.py to update your existing config.py file to the correct config version.
        - Reworked and tighten up code in the main script

* 02/29/2020 - Initial Release 1.0
    - Combined functionality of APRSTweet and APRSTelegram
    - Added: Ability to choose to send to Twitter, Telegram or All
    - Added: Ability to choose between OpenStreetMaps and Google Geocoding API for reverse geocoding of packet location
    - Added: Added the hashtag #APRS to the end of the status message for Twitter
    - Added: Finds the Maidenhead Grid Square based on packet location and includes it in the status message
    - Added: Created setup utility to help in config file creation.
    - Update: Fixed URL for aprs.fi in the status message from http:// to https://