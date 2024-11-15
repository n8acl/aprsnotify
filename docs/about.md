## Features
- Pulls most recent packet data from [APRS.fi API](https://aprs.fi/page/api) for the following types of packets:
  - Position Data
  - Weather Station Data
- Reverse Geocode with OpenStreetMaps API.
- Get Weather Conditions from WeatherAPI for the location of the position packet
- Find Maidenhead Grid Square of packet location.
- Send Status to Social Media Networks (See the Supported Services Page)
- Get notification of an APRS message sent to your station (see below for supported Networks). If someone sends a message via APRS to one of the callsigns being tracked, the script will notify you and share the message with you.

### Description

This script will pull your most recent APRS packet data from the [APRS.fi API](https://aprs.fi/page/api), will parse the data and send the data to various social media and other communications networks. The script will only pull your most recent packet and post it once.

This script can also notify you if someone/something sends you a message on APRS. This way you can stay on top and see if there are messages being sent to you by another station. This is useful, for example, for monitoring a remote station. If something trips a sensor, a message could be sent via APRS to someone and then they know that something has happened at the remote site.

Note that this bot was designed to be used by one person with multiple APRS Trackers to track packets for that one person.

If you would like to see a working example, at least on Mastodon of what the script does, please check out [@n8acl_aprs](https://mastodon.radio/n8acl_aprs) on Mastodon.

### History

This script was born many years ago out of a need to be able to let non-ham radio family members be able to track me while I was traveling to have a general idea of where I was. This was before things like Find my Friends on iPhone. I had found a similiar script back then, based in PHP (which, the developer of that script and I became friends), but after a while abandoned it and over the last few years have been developing my own version. This was out of a need to do something different than that script offered and wanting to hone my own development skills.

Earlier versions of this script were written in PHP, but after getting my first Raspberry Pi, I decided I wanted to learn Python so started porting the program to Python and have not looked back. Python is so much fun.

At one point, it only posted to Twitter and then I added Telegram as a second script. I had both up on github at one point to share with the rest of the Amateur Radio Community, but I finally realised that having everything on one code base made it so much easier to update everything last year (2020), and so APRSNotify was born. It was at that point that adding more services became a reality.

There is much more in the works for this application, so as always, stay tuned.
