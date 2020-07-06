# APRSNotify
APRSNotify is a python based bot script designed to send parsed APRS packet data to various social media accounts. This bot is a notifier and not interactive.

---

## Table of Contents
- [Features](https://github.com/n8acl/aprsnotify#Features)
- [Description](https://github.com/n8acl/aprsnotify#Description)
- [Installation](https://github.com/n8acl/aprsnotify#Installation/Setup)
- [Updating to Version 2](https://github.com/n8acl/aprsnotify#updating-to-version-2)
- [Running the Script](https://github.com/n8acl/aprsnotify#Runningthescript)
- [Credits](https://github.com/n8acl/aprsnotify#credits)
- [Contact Me](https://github.com/n8acl/aprsnotify#contact)
- [Change Log](https://github.com/n8acl/aprsnotify#changelog)

---

## Features
- Setup Utility for creating your config file.
- Pull most recent packet data from [APRS.fi API](https://aprs.fi/page/api).
- Reverse Geocode with either Google Geocoding API or OpenStreetMaps API.
- Get Weather Information from OpenWeatherMaps API for the location of the packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (currently Twitter and Telegram)
- Get notification of an APRS message sent to your station (requires Telegram to work). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and show you the message on Telegram.

---

## Description
This script will pull your most recent APRS packet data from the [APRS.fi API](https://aprs.fi/page/api), will parse the data and send the data to various social media accounts (currently either a Twitter account or to Telegram via a Telegram Bot). The script will only pull your most recent packet and post it once. Note that this was designed to be used by one person with multiple APRS Trackers to track packets from that one person.

This script can also notify you, via Telegram, if someone/something sends you a message on APRS. This way you can stay on top and see if there are messages being sent to you by another station. This is useful for monitoring a remote station. If something trips, a message could be sent via APRS to someone and then they know that something has happened at the remote site.

If you would like to see a working example, please check out [@n8acl_aprs](https://twitter.com/n8acl_aprs) on Twitter.

This script does take a little bit to get configured to run, the biggest portion of it being getting all the API keys that you will need for the script, but once those are in place, the script is very easy to run, just set it and forget it.

This script is a combination of and replaces my old APRSTweet and APRSTelegram scripts, which have now been depreciated. I decided to combine them into one to make updates and newer features easier to apply.

This script can be run from a cronjob (Linux) or Task Scheduler (Windows) and is lightweight enough to even be run on a Raspberry Pi Zero W.

Most of the instructions in this README assume that you are using Linux to setup your script to run. If you want to run it on Windows or Mac, you will need to install Python based on instructions for those OS's and know how to setup Task Scheduler, but the configuration of the script itself is the same.

### Use Cases
* Sending an APRS packet to Twitter for your followers to see.
* Sending APRS data to yourself to confirm that it is making it to the internet (via Telegram for example).
* Sending your position information to a Telegram Channel that you have your non-ham radio family and friends on so they can track you when you are traveling by car for a long distance.
* Sending position data to a radio club Telegram Channel so that everyone can see your data posted.
* Other uses that your imagination comes up with.

---

# Installation/Setup
First make sure your system is up to date
```bash
sudo apt-get update && sudo apt-get -y upgrade
```

Next you will need to install Python3 and pip3 on your system if they are not already.
```bash
sudo apt-get install python3 python3-pip
```

Next you will need to install the following python libraries if they aren't already:
```bash
pip3 install python-telegram-bot --upgrade
pip3 install Tweepy --upgrade
pip3 install geopy --upgrade
```
### API Keys Needed
Because of the nature of the API's being used, you will need to get your own API keys from the following:

* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need. Without this, nothing else will work.

* If you plan on using Telegram:
    - You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
    - You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
    - Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
    - NOTE: Telegram is required for APRS message notification to work.

* If you are planning on using Twitter:
    - You will need to get a consumer key, consumer secret, access token and access secret for the account you are wanting to post to. You can get those keys from The Twitter development site. Here is a walk through how: [Generate Twitter API Keys](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/)

* If you are planning on using Google for geocoding:
    - You will need a Google Geocoding API Key to geocode the Latitude and Longitude from your APRS Packet to get a real-time address location and weather data. [Google Geocodeing API](https://developers.google.com/maps/documentation/geocoding/get-api-key).
    - Note that Google has begun charging for calls to the API over a certain limit of calls per day. While this limit should not affect the use of the API for our use, they may make the API charge for all calls in the future.

* If you are planning on using OpenStreetMaps for Geocoding, there is not an API key required. 
    - Note that this is a free service.

* [OpenWeatherMap](https://openweathermap.org/api) to pull your weather data based on packet location data. This is a free account, but you are limited to 60 calls per minute and 1000 calls per day. You do need this for the script to work.

### Getting the Script
I recommend downloading just the aprsnotify.py, setup.py and update.py files since there is just those and it will create other files it needs. You can also clone the repo. The cloning will not update the config file only the files that are needed.

Make sure to place them in a folder that you remember. I usually use something like /scripts to keep all my small scripts in. You may want to create a scripts/aprsnotify folder to keep all related files in.

### Configure the Script
Once you have your API Keys, you can now start configuring your APRSNotify bot. To start the process, in the directory where you have the APRSNotify bot files you just downloaded/cloned, enter the command:
```bash
python3 setup.py
```
This will start the setup utility. The setup utility will walk you through the process of configuring the various needed variables and ask you for your API Keys.

You can also edit the config.py file directly in a text/python editor if you wish after it has been created. If you need a walkthrough of the configuration file for future editing, please [click here](https://github.com/n8acl/aprsnotify/blob/master/configuration.md#configuration-file-walkthrough).

---
## UPDATING TO VERSION 2

If you are updating from Version 1, you will need to run update.py to update to the new config file. Any exisiting config settings will be saved and any new config settings will be added. This is noted in the update.py utility when run. Note that a Telegram Bot is required for APRS message notification to work.

Once update.py has been run, the next time APRSNotify runs, it will delete that update.py file to helpp keep it from being run again.

---

## Running the Script
Once you have walked through the setup utility, you can run the script. To run the script, you can use the command
```bash
python3 aprsnotify.py
```
in the directory where you have the script's files. When you run this manually, you will see the status message displayed to the screen and if you look at Telegram/Twitter, you will see it there as well. This let's you know that you have everything configured correctly and everything is working fine.

Once you have confirmed that the script is running and everything is working, you can now setup to run the script automatically either via Task Scheduler in Windows or by adding a cronjob on Linux. An example of a Cronjob would be:

```bash
*/10 * * * * python3 scripts/aprsnotify/aprsnotify.py
```
In this example, my script runs every 10 minutes. My APRS beacons are sent every 5 minutes from the car, so it will post approximately every other beacon.

---

## Credits
The Telegram bot functionality is based off is a gist by Github user Lucaspg96. [Click Here](https://gist.github.com/lucaspg96/284c9dbe01d05d0563fde8fbb00db220).

The Grid Square Function was developed by Walter Underwood, K6WRU and posted on ham.stackexchange.com. [Click Here](https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square)

The map image functionality for the Telegram Bot and suggestions to include or not include Weather data amoung other suggestions were contributed by Chanyeol Yoo, Ph.D., VK2FAED

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Telegram: @ravendos
- E-mail: n8acl@protonmail.com

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log
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