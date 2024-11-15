# Getting Started

### Installation Steps
1) Setup Config file
2) Obtain API Keys
3) Install needed packages, clone Repo and install library dependencies
4) Run the Script
5) Set all other configuration options

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi, which is how I see most of these run. In fact I have mine running on a Raspberry Pi 3B+.

If you want to run this on a Windows or Mac machine, you will need to be able to install Python3 and be familiar installing from a requirements.txt.

## Obtaining API Keys

The first step in this process will be obtaining the few API keys that you need. Each service will be configured later.

##### APRS.fi API Key
* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need. Without this, nothing else will work and there is no point to the script :).
    - NOTE: There is a limit to this API. You can use 20 callsigns to find the positions/Weather of and 10 to pull messages for. Please also make sure to keep the amount of calls to a minimum. I recommend no more often than every 10 minutes. That is 6 calls an hour at max.

##### WeatherAPI Key
* Next you will need a key from [WeatherAPI.com](https://www.weatherapi.com/signup.aspx) to pull the current weather conditions for the location of the position packet. 
* Once you are signed in, your API Key will be at the top of the screen. 
  - NOTE: This is a free account, but you are limited to 1 Million API calls per month.

## Migration

If you are currently using an existing version of APRSNotfiy, you can migrate your existing database to the new version to give you a jump start on configuring things.

Please see the ```Migration Guide``` for more information.

## Installation 
Once you have these 2 keys, you can install the software. There are 2 ways to run this application
* Manual Installation - The steps listed here are for a brand new installation
* Docker Installation - The steps listed here are for a brand new installation
