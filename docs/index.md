###### Current Release 02032023

Welcome to APRSNotify - a python based bot script designed to send parsed APRS packet data to Various Social Networks. This bot was designed to be used by one person with multiple APRS Trackers to track packets for that one person.

This Wiki is designed as a user guide for the end users of the software.

This software is for use by Amateur Radio Operators Only

### Important Note

As of February 2, 2023, Twitter has announced they are no longer going to provide the free developer API starting February 9, 2023. APRSNotify will no longer support Twitter as a service due to this Starting with the 02032023 release.

### Supported Social Networks

| Function | Supported Services|
|----------|------------------|
|Position Packet Data<br>Weather Packet Data| Telegram, Mastodon, Discord, Mattermost, Slack|
|Message Notification| Telegram, Discord, Pushover, Mattermost, Slack|
|Send Packet Data<br>to Club Server| Telegram, Discord, Mattermost, Slack|

### Important Information

As you will see later in the Configuration Guide, an_til.py is a Flask Application. Flask is a Web Framework for Python that allows you to create web based applications in Python.

When you run the an_util.py, this will start a small webserver for you to connect to in order to make changes to the configurations of the script. 

I would recommend NOT exposing this web server to the outside world. It is an insecure server and only designed to be run behind a secured firewall. I would also recommend NOT leaving it running all the time for the same reason.

If you need to make changes and are not at home, I would recommend setting up a secure way to connect back into your network, preferably by a VPN, to run and make changes.

You have thusly been warned and it is now your responsibiliy to make sure you are running things securely.

### Contact Me
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Discord: Ravendos#7364
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).
