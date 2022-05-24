# Installation/Setup

### Installation Steps
1) Obtain API Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script
4) Run the Script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi, which is how I see most of these run. In fact I have mine running on a Raspberry Pi 3B+.

If you want to run this on a Windows or Mac machine, you will need to be able to install Python3, be familiar installing from a requirements.txt and be familiar with how to schedule a recurring task in those OS's.

## Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. Some of the services you choose to use may take a couple of days to approve the access to their API's (Twitter for example), so you will want to start this step before installing the script. That way when you are done installing the script and are ready to configure, you have everything ready to go.

To obtain your API keys, please see the [Obtaining API Keys](https://github.com/n8acl/aprsnotify/wiki/Obtaining-API-Keys) page in the Wiki.

Once you have your API keys for the services you plan to use, please return here.

## Installing the Script

The next step is cloning the repo to get the script and then installing the needed libraries for the script to work properly.

This is probably the easiest step to accomplish.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git

git clone https://github.com/n8acl/aprsnotify.git

cd aprsnotify

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script.

## Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring your APRSNotify bot. To start the process, run the following commands:

```bash
cd aprsnotify

python3 an_util.py
```

This will start the setup/configuration utility. The utility is now a Flask app, which means that once it is running, it will start a web server that you can connect to via a web browser and configure the script that way now. I felt this would be easier then the command line based system I used to use. All you will need to do is copy and paste the keys in when asked for them.

If in the future you want to make changes to the stored data, just run the an_util.py script again and then connect to the web server the same way.

Details about how that script works are found in the [Configuration Utility Guide](https://github.com/n8acl/aprsnotify/wiki/Configuration-Utility-Walkthrough) page on the Wiki.

## Running the Script
You will need to configure the scripts settings in the configuration utility first and once you have done that, you can run the script for a test. To run the script once, you can use the command
```bash
python3 aprsnotify.py
```
in the directory where you have the script's files. When you run this manually, you will see the latest packet you sent sent to your bot account on whatever network you are using. This let's you know that you have everything configured correctly and everything is working fine.

Once you have confirmed that the script is running and everything is working, you can now setup to run the script automatically by adding a cronjob on Linux.

Edit your crontab file:

```bash
crontab -e
```

and then add the following lines to your crontab:

```bash
*/10 * * * * python3 aprsnotify/aprsnotify.py
```

In this example, the script runs every 10 minutes. My APRS beacons are sent every 5 minutes from the car, so it will post approximately every other beacon.

On Mac and Windows, you will need to configure a scheduled task for the same effect to happen on those OS's.