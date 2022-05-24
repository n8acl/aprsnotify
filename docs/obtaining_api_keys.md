# Obtaining your API Keys

Even though this script does alot, there are alot of other webservices and networks that it needs to interact with and that is where these API, or Advanced Programmer Interface, Keys come in. An API is a service provided to allow users to programatically interact with the fore mentioned webservice.

While gathering your keys, make sure to copy them to a safe place where you can find them. You will need them for the script and some of these services can take a few days to approve your access. So please make sure to work through this and get all the keys you need saved some place before you start.

This part of the installation process, especially for a new user, takes the longest and is the most frustrating. If you already have some keys for each of these, you can use those if you choose to, to make things quicker.

Ham Radio Club/Group Server Owners: See the [Configuration for Club Servers (for Server Admins)](https://github.com/n8acl/aprsnotify/wiki/Club-Server-Admin-Guide) Guide on what is needed for API Keys for users.

**NOTE:** If you are just wanting to use this to send to a club server, the only keys you need are:
- APRS.fi
- OpenWeatherMap (if you want to include a weather report in the postion status.)

---

##### APRS.fi API Key
* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need. Without this, nothing else will work and there is no point to the script :).
    - NOTE: There is a limit to this API. You can use 20 callsigns to find the positions/Weather of and 10 to pull messages for. Please also make sure to keep the amount of calls to a minimum. I recommend no more often than every 10 minutes. That is 6 calls an hour at max.

##### OpenWeatherMap API Key
* Next you will need a key from [OpenWeatherMap](https://openweathermap.org/api) to pull the current weather conditions for the location of the position packet. 
* If you are not going to include current weather conditions in the position status message, you do not need this key. However, if you want to include this, you will need this key.
  - NOTE: This is a free account, but you are limited to 60 calls per minute and 1000 calls per day.

##### Twitter

If you are using Twitter, you are more than welcome to use your main account, however, I would recommend creating a seperate bot account for your APRS bot, like I did with [@n8acl_aprs](https://twitter.com/n8acl_aprs). That way anyone who wants to can follow you there and you don't have to clog up your main Twitter account.

* If you plan on using Twitter:
    - You will need to create a new app and get a consumer key, consumer secret, access token and access secret for the account you are wanting to post to. You can get those keys from the Twitter development site. Here is a walk through how: [Generate Twitter API Keys](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/)

##### Telegram

If using Telegram, note that any bot you have will work. For example, if you have a bot that you already use for your home automations, you could use that bot for this as well. I created a seperate bot from my home automation bot for APRS/Ham Radio use, but I could have just as easily used my home automation bot.

* If you plan on using Telegram:
    - You will need to first either create a Telegram bot or use an existing one you own. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
    - You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
    - Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
    - NOTE: Telegram is required for APRS message notification to work.

##### Mastodon

* If you plan on using Mastodon:
    - You will need to create the bot acccount first and get it approved, if the instance you are using requires approval. This must be done first before being able to obtain API keys.
    - There are many instances out there to use with Mastodon, so you will need to find one that works for you. There is a well known instance that was setup just for bots called [botsin.space](https://botsin.space). This is where I have my APRSNotify bot, but you can choose any you like.
    - Make sure you have the username, password and the instance URL where you have the bot at handy. You will need these for the configuration scripts. The nice thing about the Mastodon API wrapper is it will generate and store the keys programatically for you. All you need is to enter your login information when asked by the script.
    - The username and password is NEVER stored, just the API keys.
        - NOTE: I would recommend setting up a bot instead of using your main account for this. If something goes horribly wrong and the admin of the instance bans/locks your account, you will be out a Mastodon account till it's unlocked or un banned. If something happens to the bot account, it can be blocked and you will not loose your main account.

##### Discord

* If you plan on using Discord, you either need to have an existing server or spin up a new one up for use of you and your family and friends. These steps assume you already have a server ready to go.
* The webhook is how Discord will accept data from the script.
  - Create a new text channel for the bot (I called mine #aprs).
  - Go to the settings of your server and click on integrations (right click the server icon and go to server settings and then integrations).
  - In the middle of the screen should be a button that says "Create Webhook". Click that.
  - Give it a name (I used APRSNotify for mine) and select the new text channel you just created, or use an existing channel if you like.
  - Click the "Copy Webhook URL" button at the bottom of the window. Paste this either directly into the field in an_util, or paste this somewhere to not loose it (if you do you can come back later after creation and click the Copy button again).

##### Mattermost

* If you plan on using Mattermost, you will either need to have an existing server or spin up a new one for use of you and your familiy and friends. These steps assume you already have a server ready to go.
* Note: you will need admin access to create the Webhook Integration.
* There are a few more steps involved in setting up the Mattermost Webhook:
  - First you will need to create a new channel for the bot to post to (I called mine APRS)
  - Next, go to the hamburger menu by your name and scroll down to Integrations.
  - Here you will want to click Incoming Webhooks
  - Click "Add Incoming Hook" and then fill out the form provided. You will want to select your APRS channel and lock the bot to that channel.
  - Once you click create, a new webhook is born. The URL will be made up of two parts
    - The URL is the domain of your Mattermost server. So for example myserver.mattermost.com
    - The API key is the mix of Letter and numbers after the /hook/ part of the url showing.
  - You will need to put both of these parts into the configuration utility to be able to send to a Mattermost Webhook.

##### Pushover

* Pushover is a service that sends notifications to your phone, tablet and computer.
* **It is important to note that, while they have a free trial, it is a paid service. It is $4.99 for every platform you want to use it on after a 30 Day trial, but you only pay that $4.99 once for every platform you are using it on.**
* This is the only paid service that this app supports.
* While I am not advocating buying the service, I know that some people use it for other things already and it was an easy add to the program.
* More information about Pushover can be found [here](https://pushover.net/).
* To get your API keys for Pushover:
  * Log into your Pushover account.
  * Your User Key is the in the upper right hand corner of the screen there. Copy that someplace.
  * Next, you will need to register for an API key for Pushover to use the application with. Scroll to the bottom where it says "Your Applications" and click "Create and Application/API Token"
  * Give it a name, agree to the TOS and click create application.
  * On the next screen it shows you the API Key you will need. Copy that out and now you have the two pieces you need for message notifications to work with Pushover.

##### Slack

Like Mattermost, Slack uses Webhook URLs to allow incoming data to be posted to a channel.

* If you plan on using Slack, you will either need to have an existing server or spin up a new one for use of you and your familiy and friends. These steps assume you already have a server ready to go.
* Note: you will need admin access to create the Webhook Integration.
* Create new channel in Slack (I called my aprs)
* Click on Apps and then search for "incoming Webhook"
* Click on Add and a browser window will open.
* It will ask you to choose the server/channel to post to. Then Create the Webhook.
* Scroll down the next page down to integration settings. 
  * Double check the channel is correct
  * Copy the Webhook URL since you will need that later.
  * Give it a name (I called mine APRSNotify)
  * You can upload an Icon if you want.
  * Click Save. This will generate your incoming webhook URL.
  * Copy the URL to add to your Configuration for APRSNotify.
  * In Slack, in your channel, it will say Added Integration.

NOTE: There is a warning from Slack that this integation is legacy and may be discontinued. if that happens, APRSNotify will be updated to accomidate this change.