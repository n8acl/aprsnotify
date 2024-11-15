# Migration

If you are a current user of APRSNotify, you can migrate your database into the new format.

Note: Only the 02032023 release is supported for migration. If you are running something older then that, you will need to manually migrate your database. Start with the installation of the program as a new installation in the ```Installation Guide```

In order to migrate your database:

Copy your existing database (```aprsnotify.db```) to a new location.

```bash
cd aprsnotify

cp aprsnotify.db ~/tmp/aprsnotify.db
```

Remove the old Version of APRSNotify from your system:

```bash
rm -R APRSNotify
```

Clone the repo:

```bash
git clone https://github.com/n8acl/aprsnotify.git
```

Install dependencies:

```bash
pip3 install -r requirements.txt --break-system-packages
```

Copy the old database back into the new folder:

```bash
cd aprsnotify

cp ~/tmp/aprsnotify.db aprsnotify.db
```

Configure new database connection as described in the ```Configure the Database Connection``` of the ```Manual Installation``` Guide.

Run the ```migrate.py``` script. This will create the database and tables as well as move most of your old data from the old database.

Note that due to the way Mastodon and Mattermost are now handled, if you were using those services, this data will not be migrated and you will need to configure this by hand in the new database with the APRSNotify Configuration Utility as talked about in the ```Configuration Guide```.

```bash
python3 migrate.py
```

You can now proceed with the rest of either the manual or Docker installations.