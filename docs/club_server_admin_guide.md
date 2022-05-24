With the addition of being able to send to a club server, there might want to be clubs that allow their members to send to one channel on a server so that everyone can participate in sharing their packet information with others in the club. So server admins this is for you.

To do this, each person needs to be running their own copy of APRSNotify. Since there is a limit on the number of callsigns that can be queried with the APRS API being used, only 20 people would be able to participate if we allowed one copy to run them all. So it is easier for each person to run thier own copy.

Now this could be each person running a copy at their respective houses, or one person could run multiple copies locally, but in order to do that each person would need to provide an APRS.fi API key to the person running these copies... It is much easier to help each person run a copy at home.

Keys/Webhooks will need to be provided for each person so they can send to the server.

Here is some suggested methods for each supported service, however, do what you feel is best for your server. You are the admin, not me. These are just some ways that I think it would work well, but I am not in your server.

Also if asked, no, a person does not need to send to thier own networks to also be able to particiapte on a club server. They do need the following API Keys:
- APRS.FI
- OpenWeatherMap (if they are going to include a weather report in thier postion beacon)

## Server Configurations

### Telegram

To send to a club channel, you will need to provide users with the channel ID from Telegram.

If a user already has a bot they are using for Telegram, this bot can send to the channel. Otherwise, you will need to also provide the Bot Token to the users to allow them to use a Club Bot.

There are many ways to get the Channel ID of the Channel. Here is one suggested place to look through that gives some [options to get the Channel ID](https://stackoverflow.com/questions/33858927/how-to-obtain-the-chat-id-of-a-private-telegram-channel).

If you need to create a bot for the club, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.

This service in my opinion would be the hardest to adminstrate. If someone leaves the club or needs to be deleted from the club, If they are using the Club Bot, it would be hard to block them, unless you delete the bot and create a new one. You could block their bot from the group channel if needed however.

---

### Discord

Discord makes it very easy to do something like this. You can use one webhook, but removing someone from the channel would make it hard to administrate. I would create webhooks for each person wanting to particiapte and give them that webhook. That way if they need to be removed, all you do is delete that webhook.

Here is what I would do:

- Create a new text channel for the bot (Ex: #aprs).
- Go to the settings of the new channel (click on the gear next to the channel name or right click and go to edit channel.)
- Click Integrations on the left side.
- Click on Webhooks in the middle of the screen
- In the middle of the screen should be a button that says "New Webhook". Click that.
- Here is where it would differ between Club configuration and personal configuration. I would give the name of the webhook something that Designates it to a user. For example "N8ACL-APRS".
- Make sure under channel it is the correct channel for the APRS beacons.
- Click the "Copy Webhook URL" button at the bottom of the window. Then send it to the person it was created for. They will then need to copy into the configuration screen for APRSNotify in the Club Configuration settings for Discord.
- Click Save and you are done.

---

### Mattermost

Mattermost makes it reasonably easy to do this. You can use one webhook, but removing someone from the channel would make it hard to administrate. I would create webhooks for each person wanting to particiapte and give them that webhook. That way if they need to be removed, all you do is delete that webhook.

Here is what I would do:

- First you will need to create a new channel for the bot to post to (Ex. APRS)
- Next, go to the hamburger menu by your name and scroll down to Integrations.
- Here you will want to click Incoming Webhooks
- Click "Add Incoming Hook" and then fill out the form provided. You will want to select your APRS channel and lock the bot to that channel.
- It will ask you what username to post as. I would use the username of the person who is wanting to post to the channel.
- Once you click create, a new webhook is born. The URL will be made up of two parts
- The URL is the domain of your Mattermost server. So for example myserver.mattermost.com
- The API key is the mix of Letter and numbers after the /hook/ part of the url showing.
- You will need to send both of these parts to the user to be able to copy into their copy of APRSNotify to post to the channel.

---

### Slack

Configuring Slack is very similiar to configuring Mattermost above. Like the other services, I would consider creating webhooks for each user that wants to participate in sending packet data to the server.

Here is what I would do:

- First you will need to create a new channel for the bot to post to (Ex. APRS)
- Next, you will need to go to Apps and then look for Incoming Webhooks.
- Click on Configuration and then a webpage will open.
- Click on Add to Slack.
- Choose a channel (choose your APRS Channel) and click "Add Incoming Hook Integration" and then fill out the form provided. You will want to select your APRS channel and lock the bot to that channel.
- Scroll to the bottom.
- Copy the Webhook URL and send that to the user
- Give it a name. I would suggest something like "N8ACL-APRS"
- Click Save Settings.
- In Slack, it will show that you added the new incoming webhook integration.

If you need to remove someone from the channel, repopen the Incoming Webhook configuration in a browser, select the webhook to delete and then click remove.

NOTE: There is a warning from Slack that this integation is legacy and may be discontinued. if that happens, APRSNotify will be updated to accomidate this change.