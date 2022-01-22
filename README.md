# APRSNotify
###### Current Release 01222022
APRSNotify is a python based bot script designed to send parsed APRS packet data to various Social Media or Communications networks.

This software is for use by Amateur Radio Operators only.

This bot was designed to be used by one person with multiple APRS Trackers to track packets for that one person.

Please see [the Wiki](https://github.com/n8acl/aprsnotify/wiki) for more information and [installation](https://github.com/n8acl/aprsnotify/wiki/Installation) and [configuration](https://github.com/n8acl/aprsnotify/wiki/Configuration-Utility-Walkthrough) steps as well as [running the script](https://github.com/n8acl/aprsnotify/wiki/Running-The-Script).

##### Working Examples:
- Twitter: [@n8acl_aprs](https://twitter.com/n8acl_aprs)
- Mastodon: [You will need to follow n8acl_aprs@botsin.space.](https://botsin.space/@n8acl_aprs)

##### Currently Supported Networks/Functions

| Function | Supported Services|
|----------|------------------|
|Position Packet Data<br>Weather Packet Data| Twitter, Telegram, Mastodon, Discord, Mattermost, Slack|
|Message Notification| Telegram, Discord, Pushover, Mattermost, Slack|
|Send Packet Data<br>to Club Server| Telegram, Discord, Mattermost, Slack|

---

## Features
- Pulls most recent packet data from [APRS.fi API](https://aprs.fi/page/api) for the following types of packets:
  - Position Data
  - Weather Station Data
- Reverse Geocode with OpenStreetMaps API.
- Get Weather Conditions from OpenWeatherMaps API for the location of the position packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (See above for supported Networks)
- Get notification of an APRS message sent to your station (see above for supported Networks). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and share the message with you.
- Send packet data to a club Server channel. This allows club members to share packet data information with each other.

---

### Use Cases
* Sending an APRS packet to Twitter/Mastodon for your followers to see.
* Sending Weather data from APRS to Social Media.
* Sending APRS data to yourself to confirm that it is making it to the internet.
* Sending your position information to a Telegram/Discord/Mattermost/Slack Channel that you have your non-ham radio family and friends on so they can track you when you are traveling by car for a long distance.
* Participating in sending packet data to a club server/channel in addition to your own channels/servers
* Other uses that your imagination comes up with.

---

## UPGRADE TO RELEASE 01212022

To upgrade to the current version of the script, please run the update.py script. It will update your database to the most current version.

If you are installing the whole script for the first time (i.e. have never used APRSNotify before), please run an_util.py instead. Only run the upgrade script if you have used APRSNotify before and have previously upgraded to version 4.

#### Upgrading a version older than Version 4 to current version

Please note that any version prior to 4 has had to be depreciated and is no longer supported. With all the changes, it is difficult to support those older versions with the new version.

The easiest way to upgrade a version of APRSNotify that is older than Version 4 is to make sure to backup the config.py file to another location and then deleting the old APRSnotify script folder. Then clone the repo to get the latest script files. This allows you to setup the script as basically a brand new setup, just follow the directions in the wiki for a new setup and using the an_util.py file. You can use your old config.py file as reference to copy and paste your keys and things in as needed.

---

## Credits
The Original Telegram Notify bot functionality was based off a gist by Github user Lucaspg96. [Click Here](https://gist.github.com/lucaspg96/284c9dbe01d05d0563fde8fbb00db220).

Adding Grid Square to Status message was suggested by Alex, N7AGF.

The Grid Square Function was developed by Walter Underwood, K6WRU and posted on ham.stackexchange.com. [Click Here](https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square)

The map image functionality for the Telegram Bot and suggestions to include or not include Weather data among other suggestions were contributed by Chanyeol Yoo, Ph.D., VK2FAED

APRS.FI API Limitations issues found and troubleshot by [Alex Bowman, KN4KNG](https://github.com/KN4KNG). 

Installation of the Verison 4 scripts troubleshot by Diego, EA3ICN.

Pushover mechanics from [Micheal Clemens, DL6MHC](https://qrz.is/)

APRS and the APRS System and associated copyright were developed by Bob Bruninga, WB4APR [http://www.aprs.org](http://www.aprs.org).

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Discord: Ravendos#7364
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log

* 01/21/2022 - Release 01212022
  - Added Support for Slack
  - Added Messaging support for Mattermost, Slack
  - Added Support to send to Club Servers (See above networks table for supported networks)
  - Added ability to find current release number from command line
  - Changed versioning system to date of release (similar to Home Assistant and other applications)
  - Fixed Various bugs found
  - Updates to Wiki
    - Added Club Configuration and how to for server admins to allow club members to send to the server.
    - Moved Change Log entres prior to 2022 [to a wiki page](https://github.com/n8acl/aprsnotify/wiki/Change-Log). This is to help clean up the README File a little.

* 01/16/2022
  - Fixed issue with weather part of the status message

* 01/15/2022 - Minor update
  - Fixed error in message sending to Pushover
  - Fixed error in packet status creation with fixed station
  - Fixed error in sending messages notification via Discord

* 01/12/2022 - Version 6.0 Release
  - Added support for Discord and Pushover for Message Notitification
  - Added Support for Mattermost for Position and Weather packet data
  - Split out configuration for message notification to new screen in Config Utility
  - Added number of callsigns in the callsign lists on Config Utility
  - Added the prevention of adding more callsigns then able to be handled by aprs.fi api
  - Pull version number from database for Config Utility