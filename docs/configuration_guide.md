# Configuration Utility

### Running the Utility

Running the utility can be accomplished either manually or with Docker. If you are using Docker, the utility container was created when everything was spun up. You will only need to connect to the webaddress to access the utility.

Please note that if you are using Docker, you will not need to manually start the utility program to make changes. The utility will be available aslong as you leave the container running. If you stopped the container, you will need to restart it to access the utility to make changes.

To run the utility manually, in the directory where you have the scripts files, please run the following command in the terminal or command line:

```bash
cd aprsnotify/an_util

python3 an_util.py
```

You will need to then leave this window open to keep the program running while you are making changes. If you close the window, the script will stop and then you will not be able to connect to the application to make changes.

#### Disclaimer

As stated on the front page of the Wiki, when you run the an_util.py, this will start a small webserver for you to connect to in order to make changes to the configurations of the script.

I would recommend NOT exposing this web server to the outside world. It is an insecure server and only designed to be run behind a secured firewall. 

If you need to make changes and are not at home, I would recommend setting up a secure way to connect back into your network, preferably by a VPN, to run and make changes.

You have thusly been warned and it is now your responsibiliy to make sure you are running things securely.

## Connecting to the Utility

an_util is a Flask app. Flask is a web framework in Python that basically allows you to run a python application as a web application. As such, you will need a web browser to work with the configuration utility.

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

To navigate through any of the menus in the program, just click on the selection you want.

#### 1: Main Menu

When you first connect to the utiltiy from the browser, you are presented with one of 2 following screens:

If you are NOT using the Apprise-API for notification management, you will see the following:

![image](https://github.com/user-attachments/assets/738d492a-12ad-46b2-9baa-c981d78d5ed0)

If you ARE using the Apprise-API, you will see the following:

![image](https://github.com/user-attachments/assets/07509ba6-f0f1-46e9-b2a3-1ec8a36609ad)

This is the main menu. From here you can select where to go. Just click on the option you want to configure.

#### 2: Main Program Configuration Settings

After choosing this option, you are presented with the following screen:

![image](https://github.com/user-attachments/assets/2579297b-b2db-42ed-8eff-71e859d91653)


Here you can set the following options:

- Units to use - This lets you set whether to use Imperial (inches, feet, miles, Fahrenheit) or Metric (Kilomoters, meters, Celcius)
- Time to wait for Checks (in seconds) - This sets how long the program should wait to check for new packets. Default is 600 Seconds (10 Minutes).
  - Note that the minimum allowed time is 600 seconds. This is to be nice to the APRS.Fi and WeatherAPI APIs.
- Your Timezone - Set your Timezone here.
- Use Apprise-API - If you are using the Apprise-API for notification management, turn this on. (Note this changes the Main Menu screen to show the Apprise-API links)
- APRS.Fi API Key - This is your APRS.Fi API Key, obtained during the ```Obtain API Keys``` Step
- WeatherAPI API Key - This is your WeatherAPI.com API key, obtained during the ```Obtain API Keys``` Step


#### 3: Callsign Tracking List Configuration

After choosing this option, you will be presented with the following menu:

![image](https://github.com/user-attachments/assets/815febd6-66d1-43b5-9e79-85479272ecb4)

Here is where you can add or delete callsigns from tracking for the different lists.

***Adding***
Note that when adding a station, you need to include the SSID of the station. The application will not do a fuzzy search.
ex: N8ACL-9

Also, when adding a station, make sure to select the correct list from the drop down at the end of the line.

Hit Add

***Deleting***
When deleteing, select the callsign you want to remove from the drop down and then select what list you want it removed from in the next drop down.
Make sure to double check that is the callsign you want to remove. Once you confirm the deletion, there is no way to go back and recover it. You will need to re-add it.

### 4: Configure Social Media Services

After Selecting this option, you will be presented with a menu similar to this one:

![image](https://github.com/user-attachments/assets/fda9ed8e-da05-47e4-9632-885c3a004c93)

This allows you to select one of the supported services to add a new one. Once you click on a button, you will be taken to a screen similar to this:

![image](https://github.com/user-attachments/assets/5bab659f-e136-45da-8fe2-f6edb6b7de4c)

Each Service will be a little different. In order to add a new service, please make sure to enter all the information that is asked for on the screen.

### 5: Update Your Existing Services

When you click on this option, you will be presented with a screen similiar to this:

![image](https://github.com/user-attachments/assets/0565cb26-9e8d-4508-a119-65ad6991316c)

This will list all your currently configured services. From here, you will be able to select which one of the services/links that you want to update. By clicking on one of the update buttons at the end of the line, this will bring you to a screen similiar to this:

![image](https://github.com/user-attachments/assets/a5b72107-8613-49cc-b54a-48d2083f95f2)

Each configured service will be a little different. Make your changes to that service and then click submit. This will update that services data.

### 6: Configure Apprise-API (Advanced Feature)

Note that this feature is for advanced users.

If you want to use the Apprise-API for notification management, you will need to first have Apprise and Apprise-API setup on a server somewhere. Then you will need to make sure to configure some services in there to use. Make sure to set tags for each type of notification that APRSnotify uses (POS, WX and MSG).

So for example, if you have a personal and club service setup for position reporting, you will need to tag the two urls and then add then to one tag. This is all explained in the [Apprise-API documentation](https://github.com/caronc/apprise-api).

When you click on this option, you will be presented with a screen similiar to this:

![image](https://github.com/user-attachments/assets/9c4796dd-b210-45f2-bafa-8df6e33b5ccd)

Here you will need to enter the following:

- Apprise-API URL: This is the URL of your Apprise-API service.
- Apprise-API Config Key: This is the key name of the config that APRSNotify should look for the service URLs that were setup.
- Apprise-API Position Tags: This is a list of tags that can be used to send position reports to.
- Apprise-API Message Tags: This is a list of tags that can be used to send message reports to.
- Apprise-API Weather Tags: This is a list of tags that can be used to send weather reports to.

If a tag type is not used, you can either leave the default or clear it out.

### Ending the program

Once you are done with configuring options, you can just close your web browser.

If you started the program manually, you will need to hit CTRL-C in the terminal window you left open to exit the program.

Otherwise if running in Docker, just leave it alone.