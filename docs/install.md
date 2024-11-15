## Manual Installation

These steps are for a brand new installation. If you want to migrate your data, see the ```Migration Guide``` then come back here and go to the ```Configure the Script``` section.

Manual installation will allow you to run the script directly from the command line and let it run.

To install the script please run the following commands:

First install needed packages:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen
```

Clone the repository:

```bash
git clone https://github.com/n8acl/aprsnotify.git
```

Switch to the repository and install the required Python Packages:

```bash
cd aprsnotify

pip3 install -r requirements.txt
```
### Configure the Database Connection

APRSNotify supports the use of MySQL/MariaDB, PostgreSQL, Microsoft SQL Server and Sqlite databases for configuration management. Of these, Sqlite does not need a username and password setup for the script to access the database. However the others do. You will need to setup a user in your database system before setting up the database connection.

It is recommended to NOT use any System Administrator accounts or any account that has administrative rights on your Database system. You should create a user account that has at least the following privileges:
- Create Database
- Create Tables
- Select, Insert, Update, and Delete on tables.

Once you have the user created, edit the ```config.json``` file in your favorite editor. Here we will need to set the database connection settings. 

```json
{
  "database": {
    "rdbms_type": "",
    "credentials": {
      "username": "",
      "password": "",
      "host": ""
    }
  }
}
```

We will need to update the following settings:

- ```"rdbms_type": "",``` - set this to one of the following settings, depending on the database management system you want to use:
    - ```sqlite``` - This is the default database that is used by Python. This creates a database file in your APRSNotify folder. Use this if you don't have another Database solution.
    - ```mysql``` - This will connect to MySQL/MariaDB. This is a free open source Database Management System.
    - ```postgresql``` - This will connect to PostgreSQL. This is another free open source Database Management System.
    - ```mssql``` - This will connect to Microsoft SQL Server. This is normally a paid for product, but SQL Server can be used with a devloper licence for personal use, IE it is not being used for in a business production environment.
- ```"username": "",``` - This is the user that can connect to your database. Note this is optional for SQlite databases only.
- ```"password": "",``` - This is the password for the user account above. Note this is optional for SQlite databases only.
- ```"host": ""``` - This is the FQDN or IP Address of the Database server host.

Save the file and then run the install script to create the database:

```bash
python3 install.py
```

Now you have everything installed and are ready to configure the script.

## Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring your APRSNotify bot. To start the process, run the following commands:

```bash
cd aprsnotify

python3 an_util.py
```

This will start the setup/configuration utility. The utility is a Flask app, which means that once it is running, it will start a web server that you can connect to via a web browser and configure the script that way.

If in the future you want to make changes to the stored data, just run the an_util.py script again and then connect to the web server the same way.

Details about how the configuration utility works are found in the [Configuration Utility Guide](https://github.com/n8acl/aprsnotify/wiki/Configuration-Utility-Walkthrough) page on the Wiki.

## Running the Script
You will need to configure the scripts settings in the configuration utility first and once you have done that, you can run the script for the first time. To run the script, you can use the following commands

```bash
screen -R aprsnotify

python3 aprsnotify.py
```

in the directory where you have the script's files. When you run this, you will see the latest packet you sent sent to your bot account on whatever network(s) you are using. This let's you know that you have everything configured correctly and everything is working fine.

The script will continue to run, checking for new packets every 10 minutes (600 second) by default and then sending the packet out. This can be changed, but 10 minutes is the minimum the script will except. This is sufficent to give people an idea of where you are/Where you have been. This is not meant to be a realtime tracker. If you have your mobile station set to send packets every 5 minutes as you drive, 10 minute checks means that at least every other packet will be sent. 10 Minutes also allows us to be nice to the API that we are using to check for packets.

If you notice that you are not sending packets all of a sudden, please check to make sure that the script did not error out with:

```bash
screen -R aprsnotify
```

If it errored out, you can restart it with:

```bash
python3 aprsnotify.py
```