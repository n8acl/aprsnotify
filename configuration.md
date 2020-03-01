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