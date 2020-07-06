# Configuration File Walkthrough

First you will need to choose the service(s) you wish to send the packet to. Set the send_status_to variable based on the service(s). Default is 0 (all):
```python
## select which service to send the status to. Default is 0 (all):
# 0 = All
# 1 = Twitter
# 2 = Telegram
send_status_to = 0
```

Next you will need to choose the Geocoder API you wish to use. Set the geocoder_to_use variable appropriatly. Default is 2 (OpenStreetMaps):
```python
## Select Geocoder to use. Default is 2 (OpenStreetMaps):
# 1 = Google
# 2 = OpenStreetMaps
geocoder_to_use = 2
```
Next choose the units you want to use, either metric (Degrees C, Kilometers Per Hour, etc) or Imperial (Degrees F, Miles per hour, Etc). Default is 2 (Imperial):
```python
## Select Unit Type to use. Default is 2 (Imperial):
# 1 = Metric
# 2 = Imperial
units_to_use = 2
```

Want to be notified if an APRS Message is sent to a station in your list? Enable it here. Please note that this does require Teleggram to use. Not all messages to your station need to go to Twitter. Default is 0 (No):
```python
## Enable APRS Message notification. Default is 0 (No):
## Note: You must provide a Telegram Bot Key and Chat ID below for messaging notification to work.
# 0 = No
# 1 = Yes
enable_aprs_msg_notify = 1
```
Do you want to include a map image in your status? Currently this only works with Telegram, but it is kind of cool to see. This would be useful if you are pushing your APRS packet to a club Telegram channel for example or to a family Telegram Channel for others to see. Default is 0 (No):
```python
## Include Map image in status. Default is 0 (No):
## Note: You must provide a Telegram Bot Key and Chat ID below for messaging notification to work.
# 0 = No
# 1 = Yes
include_map_image = 1
```

Do you want to include a weather report for the location of the packet in your status message to Twitter or Telegram? Default is 1 (Yes):
```python
## Include Weather information in status. Default is 1 (Yes):
# 0 = No
# 1 = Yes
include_wx = 1
```

If you are using Twitter, you will need to add your keys to the config file:
```python
## Configure Twitter Keys
twitterkeys = {
    "consumer_key": "YOUR CONSUMER KEY HERE",
    "consumer_secret": "YOUR CONSUMER SECRET KEY HERE",
    "access_token": "YOUR ACCESS TOKEN HERE",
    "access_secret": "YOUR ACCESS SECRET KEY HERE"
}
```

If you are using Telegram, you will need to add your bot token and chat ID to the config file:
```python
## Configure Telegram Keys

telegramkeys = {
    "my_bot_token": "YOUR BOT TOKEN HERE", #token that can be generated talking with @BotFather on telegram for your bot
    "my_chat_id": "YOUR CHAT ID HERE" # chat_id must be a number!
}

```

Finally, you will need to configure the last of the variables in the config file:
```python
## Configure Other API Keys and Variables

callsign_list = ["CALLSIGN-1","CALLSIGN-2"] # This is the list of callsigns with ssid to monitor and tweet. You need at least one but can be as many as you want separated by commas
aprsfikey = "YOUR APRS.FI API KEY" # This is your API key from your APRS.fi account
googlegeocodeapikey = "YOUR GOOGLE GEOCODING API KEY HERE" # this is your Google Geocodeing API Key from
openweathermapkey = "YOUR OPENWEATHERMAP API KEY HERE" # This is your OpenWeatherMap API Key.
```
- **callsign_list**: This is the list of callsigns, with SSID, you wish to track, separated by commas. Example: "N8ACL-9","N8ACL-6". You can track as many callsigns here as you wish
- **aprsfikey**: This is the API key from your APRS.FI account page. 
- **googlegeocodeapikey**: This is the API key from the Google Geocoding API.
- **openweathermapkey**: This is the API key from OpenWeatherMaps.