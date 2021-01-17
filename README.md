# APRSNotify
APRSNotify is a python based bot script designed to send parsed APRS packet data to Twitter, Telegram and/or Mastodon.

This software is for use by Amateur Radio Operators only.

Please see the Wiki for more information and installation and configuration.

##### Working Examples:
- Twitter: @n8acl_aprs
- Mastodon: You will need to follow n8acl_aprs@botsin.space.

---

## Features
- Pulls most packet data from [APRS.fi API](https://aprs.fi/page/api) for the following types of packets:
  - Position Data
  - Weather Station Data
- Reverse Geocode with OpenStreetMaps API.
- Get Weather Information from OpenWeatherMaps API for the location of the position packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (currently Twitter, Telegram and Mastodon)
- Get notification of an APRS message sent to your station (requires Telegram to work). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and show you the message on Telegram.

---

### Use Cases
* Sending an APRS packet to Twitter/Mastodon for your followers to see.
* Sending Weather data from APRS to Social Media.
* Sending APRS data to yourself to confirm that it is making it to the internet (via Telegram for example).
* Sending your position information to a Telegram Channel that you have your non-ham radio family and friends on so they can track you when you are traveling by car for a long distance.
* Sending your APRS data to a club Mastodon Instance feed for the club to see.
* Sending position data to a radio club Telegram Channel so that everyone can see your data posted.
* Other uses that your imagination comes up with.

---

## UPGRADE TO VERSION 4.0

To upgrade to version 4.0 of the script, please run the updatev4.py script. It will pull in everything from the old config.py file that it can. 

Please make sure to backup the config.py file before cloning the repo again to get the latest script files. It shouldn't delete it, but it may, so please make sure to backup the config file first and then copy it back in if needed before running updatev4.py.

If you are installing the whole script for the first time (i.e. have never used APRSNotify before), do not run this script, but please run an_util.py. Only run this upgrade if you have used APRSNotify before and have an existing config.py file.

Due to some changes to meet the APRS.fi API requirements, I have had to split the callsign list into 3 lists, a postion tracking list, a message notification list and now, if you have a weather station that puts weather data on APRS, a weather station tracking list. There can only be 20 callsigns to track positions with and 10 to get messages with. Because of this, we cannot automtically bring the lists in and will need you to reenter them when asked by the update utility.

The update utility will also ask if you want to send the status to Mastodon, then ask you to set that up. Please make sure that you have followed the directions in the wiki to obtain the API keys for Mastodon if you are going to use that before running the update script. 

---

## Credits
The Original Telegram Notify bot functionality was based off a gist by Github user Lucaspg96. [Click Here](https://gist.github.com/lucaspg96/284c9dbe01d05d0563fde8fbb00db220).

Adding Grid Square to Status message was suggested by Alex, N7AGF.

The Grid Square Function was developed by Walter Underwood, K6WRU and posted on ham.stackexchange.com. [Click Here](https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square)

The map image functionality for the Telegram Bot and suggestions to include or not include Weather data among other suggestions were contributed by Chanyeol Yoo, Ph.D., VK2FAED

APRS.FI API Limitations issues found and troubleshot by [Alex Bowman, KN4KNG](https://github.com/KN4KNG). 

APRS and the APRS System and associated copyright were developed by Bob Bruninga, WB4APR [http://www.aprs.org](http://www.aprs.org).

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Telegram: @ravendos
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@protonmail.com

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log
* 01/15/2021 - Version 4.0 Release
    - Removal of APRSBot to a different project
    - Moved from text files for data storage to SQLlite3 Database
    - Various small bug fixes and rework of the code.
    - Added: ability to send status to Mastodon
    - Added: an_util.py configuration utility for interacting with the database
    - Added: New wiki user guide.
    - Added: Parsing of Weather Data packet from APRS.

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
