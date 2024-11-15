# Docker Installation (Recommended)

If you want to migrate your data, see the ```Migration Guide``` then come back here and build the containers, then go to the ```Run the Containers``` section.

In order to use the docker containers, you will need to build them locally.

This assumes that you already have Docker and Docker Compose installed. If you do not, you will need to install those for the operating system you are running. There are many tutorials online on how to do this.

Clone the repo and then enter into that new directory:

```bash
git clone https://github.com/n8acl/aprsnotify.git

cd aprsnotify
```

### Building

Next, using Docker Compose, let's build the containers:

```bash
docker compose build
```

### Configure the Database Connection

APRSNotify supports the use of MySQL/MariaDB, PostgreSQL, Microsoft SQL Server and Sqlite databases for configuration management. Of these, Sqlite does not need a username and password setup for the script to access the database. However the others do. You will need to setup a user in your database system before setting up the database connection.

It is recommended to NOT use any System Administrator accounts or any account that has administrative rights on your Database system. You should create a user account that has at least the following privileges:
- Create Database
- Create Tables
- Select, Insert, Update, and Delete on tables.

Once you have the user created and the containers built as noted above, edit the ```config.json``` file in your favorite editor. Here we will need to set the database connection settings. 

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

Save the file.

### Run the Containers

Make sure to modiy the volume directives in the ```docker-compose.yaml``` file to point to the correct path for your aprsnotify directory.

Now we just need to bring up the containers:

```bash
docker compose up -d
```
