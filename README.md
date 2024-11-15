# APRSNotify2

###### Current Release 1.0.0

APRSNotify is a python based bot script designed to send parsed APRS packet data to various Social Media or Communications networks.

This software is for use by Amateur Radio Operators only.

This bot was designed to be used by one person with multiple APRS Trackers to track packets for that one person. It is possible to send to multiple services as well. Send to as many places as you want.

There are SEVERAL Updates that have been made to the software. Please make sure to read the Change Log below for all the changes.

Please see [the Wiki](https://n8acl.github.io/aprsnotify) for more information and installation and configuration steps as well as running the script.

##### Working Examples:
- Mastodon: [You will need to follow n8acl_aprs@mastodon.radio.](https://mastodon.radio/@n8acl_aprs)

##### Currently Supported Networks/Functions

To see the list of netowrks supported direcetly in APRSNotify, please see the Supported Services Page on [the Wiki](https://n8acl.github.io/aprsnotify/aupported_services/). This list will be growing.

APRSNotify2 now uses the Apprise python library to send notifications to the different messageing services. Apprise supports over 100+ different services, so adding new services is a lot easier. These services above are supported within APRSNotify currently. While Apprise does support way more services, implementation has to be done in the app for each service. 

However, there is a huge advantage to using Apprise now. If you are like me and use the Apprise libray and have the Apprise-API running on your network for other notifications, that can be leveraged to send notifications with APRSNotify. This allows users that use the Apprise-API access to all the services that Apprise supports. For more information about that, see [the Wiki](https://n8acl.github.io/aprsnotify).

---

## Features
- Pulls most recent packet data from [APRS.fi API](https://aprs.fi/page/api) for the following types of packets:
  - Position Data
  - Weather Station Data
  - Message Data
- Reverse Geocode Packet loction with OpenStreetMaps API.
- Get Weather Conditions from WeatherAPI.com for the location of the position packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (See above for supported Networks)
- Get notification of an APRS message sent to your station (see above for supported Networks). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and share the message with you.

---

### Use Cases
* Sending an APRS Position packet to Social Media for your followers to see.
* Sending Weather data from APRS station to Social Media.
* Sending APRS data to yourself to confirm that it is making it to the internet.
* Sending your position information to a Channel that you have your non-ham radio family and friends on so they can track you when you are traveling by car for a long distance.
* Participating in sending packet data to a club server/channel in addition to your own channels/servers
* This could potentially be used to track up to 20 mobile stations during a race or parade and relay that information to others, like officials or other hams working in the race. (Note though that this program does not support the use of tactical callsigns. The callsigns must be Call-ssid to be tracked.)
* Other uses that your imagination comes up with.

---

## UPGRADE TO CURRENT RELEASE

Due to the massive amount of changes done to the codebase, only the last version release of the APRSNotify1 software is supported for migration. If you have something older, you will need to install this as a clean install and then manually migrate your data over.

For Migration steps, see [the Wiki](https://n8acl.github.io/aprsnotify/migration/).

---

## Credits
The Original Telegram Notify bot functionality was based off a gist by Github user Lucaspg96. [Click Here](https://gist.github.com/lucaspg96/284c9dbe01d05d0563fde8fbb00db220).

Adding Grid Square to Status message was suggested by Alex, N7AGF.

The Grid Square Function was developed by Walter Underwood, K6WRU and posted on [ham.stackexchange.com](https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square).

The map image functionality for the Telegram Bot and suggestions to include or not include Weather data among other suggestions were contributed by Chanyeol Yoo, Ph.D., VK2FAED (Though this had been deprecated in APRSNotify now, still wanted to give credit to include it originally.)

APRS.FI API Limitations issues found and troubleshot by [Alex Bowman, KN4KNG](https://github.com/KN4KNG). 

Installation of the APRSNotify1 Verison 4 scripts troubleshot by Diego, EA3ICN.

Pushover Notification API mechanics from [Micheal Clemens, DL6MHC](https://qrz.is/)(Though this had been deprecated in APRSNotify now, still wanted to give credit for the idea to include it originally.)

The [Apprise library](https://github.com/caronc/apprise) and [Apprise-API](https://github.com/caronc/apprise-api) were created and maintained by Chris Caron.

APRS and the APRS System and associated copyright were developed by Bob Bruninga, WB4APR (SK) [http://www.aprs.org](http://www.aprs.org).

---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Discord: Ravendos
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log 
Changes Prior to current year have been moved to the [ChangeLog](https://n8acl.github.io/aprsnotify/changelog/) on the wiki.

## Version 1.0.0 - Released 10/30/2024
## Added
- Now uses the Apprise notification library for service notifiction support. 
  - This makes adding new services easier
  - Also allows for multiple destinations for a service
  - Can leverage the Apprise-Api to allow the user to completely configure and manage their own notification services.
- Added support for sending to the following services (if using the Apprise service included with APRSNotify):
  - DAPNET
  - Matrix
  - Signal
- Added Database support for the following Database Managment Systems for configuration management
  - Microsoft SQL Server
  - MySQL
  - PostgreSQL
  - SQLite
- Support for running in Docker

## Changed
##### APRSNotify
- Changed version numbering scheme back to Major.Minor.Build format (ex 2.0.0)
- Changed how Mastodon connections are handled
- Changes how Mattermost connections are handled
- Always includes weather information in postion report now
- Move from OpenWeatherMap to WeatherAPI.com for weather information

##### APRSNotify Utility
- Complete rework of the HTML Templates and Backend utility functions.


## Removed
- Removed option to exclude weather information from postion report
- Removed Support of OpenWeatherMap for Weather Data
- Removed support of sending map image with Telegram messages

