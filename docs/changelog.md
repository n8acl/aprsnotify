* 05/30/2021
  - Minor updates to README and the wiki. 

* 05/19/2021 - Version 5.0 Release
  - Update of APRSNotify Database to consolidate callsign lists to one table
  - Redesign of an_util.py into a Flask app to allow for web browser based GUI to configure the script.
  - Addition of Discord to supported networks.
  - Automatically does not send a map image with WX Station Data or message notification to Telegram
  - Updated Wiki with new information.

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