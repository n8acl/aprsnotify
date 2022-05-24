# Configuration Utility

### Running the Utility

To run the utility, in the directory where you have the scripts files, please run the following command in the terminal or command line:

```bash
python3 an_util.py
```

You will need to then leave this window open to keep the program running while you are making changes. If you close the window, the script will stop and then you will not be able to connect to the application to make changes.

#### Disclaimer

As stated on the front page of the Wiki, when you run the an_util.py, this will start a small webserver for you to connect to in order to make changes to the configurations of the script.

I would recommend NOT exposing this web server to the outside world. It is an insecure server and only designed to be run behind a secured firewall. I would also recommend NOT leaving it running all the time for the same reason.

If you need to make changes and are not at home, I would recommend setting up a secure way to connect back into your network, preferably by a VPN, to run and make changes.

You have thusly been warned and it is now your responsibiliy to make sure you are running things securely.

## Connecting to the Utility

an_util is a Flask app. Flask is a web framework in Python that basically allows you to run a python application as a web application. Since an_util is now in Flask, you will need a web browser to work with the configuration utility now.

The webserver for an_util runs on port 5001. So if you have this running on a Raspberry Pi for example, you would use the ip address of the Pi and port 5001.

So you will need to enter the ipaddress and port number of 5001 of the server into your web browser like the following:

```bash
http://10.0.0.1:5001
```

From there, it works just like a regular website.

If you need to find the IP Address of the machine you are running the utility on, in Linux, you can type the following command:

```bash
ifconfig
```
and it will display the IP address of your device.

To navigate through any of the menus in the program, just click on the selection you want and then hit enter.

#### 1: Main Menu

When you first connect to the utiltiy from the browser, you are presented with the following screen:

![Screen Shot 2022-01-22 at 01 35 20](https://user-images.githubusercontent.com/40501228/150627923-409a9112-8b54-41e2-876d-3bedf1b49313.png)

This is the main menu. From here you can select where to go. Just click on the option you want to configure.

#### 2: Main Program Configuration Settings

After choosing this option, you are presented with the following screen:

![Screen Shot 2022-01-22 at 01 36 45](https://user-images.githubusercontent.com/40501228/150627959-565722e6-bb18-4397-ab37-3384b94f95a2.png)



Here you can set the following options:

- Units to use - This lets you set whether to use Imperial (inches, feet, miles, Fahrenheit) or Metric (Kilomoters, meters, Celcius)
- Include Weather in Status - This allows you to choose whether or not you want to include a weather report with the packet status. Sometimes you may not want to include this.
- Send Postition Data - If you are going to use this program to send position data to the networks, turn this on.
- Send Weather Data - If you are using this to post the weather data from a fixed weather station, turn this on.


#### 3: Callsign Tracking List Configuration

After choosing this option, you will be presented with the following menu:

![Screen Shot 2022-01-22 at 01 37 26](https://user-images.githubusercontent.com/40501228/150627994-f39248dc-bddb-40be-8df0-7c9253131fd7.png)

Here you can add and delete from each of the lists as needed. To add just select the add option or delete the delete option and then select the list you want to modify and then enter the list of callsigns you want to add, seperated by commas.

Example: "Add to POS Callsign List the following Callsigns: n8acl-9, n8acl-6, n8acl"

### 4: Configure Social Media Services

After Selecting this option, you will be presented with a menu similar to this one:

![Screen Shot 2022-01-22 at 01 38 18](https://user-images.githubusercontent.com/40501228/150628019-97e571ef-d8d8-4ec3-b98e-f5defa18e348.png)

This is a very long screen, but this is where you will configure most all the networks that APRSNotify will send to. All you need to do is enter the information asked for for the services you want to use and click the submit button in the box of that service.

So for example, if you want to modify the keys for Telegram, you would select Yes, paste the tokens into the appropriate fields or decide if you want to use Map inclusion and click submit.

The options for Mastodon are a little bit different. In order to change the tokens for this service, you need to enter the information asked for in the fields and when you click submit, the program will go out and generate the correct keys for you. ONLY DO THIS IS IF YOU ABSOLUTLY NEED NEW KEYS.

### 5: Configure Messaging Notification Services

When you click on this option, you will be presented with a screen similiar to this:

![Screen Shot 2022-01-22 at 01 39 45](https://user-images.githubusercontent.com/40501228/150628062-0a58a9da-f23e-4933-867a-85aaf66d775b.png)

This is where you set your options and where you would like the message Notification to go to.

Note: The Bot keys for Telegram are the same ones that would be used for packet data, so these are already filled in for you from when you configured those.

I would recommend for Discord, Mattermost and Slack, setting a private channel on your server that only you have access to for the APRS message notifications. However, like Telegram, you can use the existing webhook if you like, but the messages will be sent to the public channel.

### 6: Configure Club Services

When you click on this option, you will be presented with a screen similiar to this:

![Screen Shot 2022-01-22 at 01 41 39](https://user-images.githubusercontent.com/40501228/150628128-7f8c7b52-79bd-4838-aacb-31d84f5a7923.png)

If your club runs one of these servers, and allows it, this would allow for the option for members to be able to send to packet information to a channel on that server. The server admin would need to provide you with keys or webhook url's to be able to paricipate.

### 7: Configure Various API Keys

When you select this option, you will get a screen similiar to the following:

![Screen Shot 2022-01-22 at 01 44 45](https://user-images.githubusercontent.com/40501228/150628195-8425979f-221d-4722-b686-5c9dbd412653.png)

Here is where you can paste your APRS.Fi API key and your OpenWeatherMap API Key. Click submit under the appropriate category to store the keys.

### Ending the program

At any time, if you hit CTRL-C in the terminal window you left open, you can exit the program.