#!/bin/bash

# This script will use screen to start the bot running. I like to run this in screen so that if there is a 
# problem or I need to shut down the bot and restart it, I can connect to that screen session and 
# take care of it this can be accomplished by:
#
# screen -R aprsbot

sleep 1m
screen -dmS aprsbot
screen -S aprsbot -p 0 -X stuff "cd /home/pi/scripts/aprsnotify$(printf \\r)"
screen -S aprsbot -p 0 -X stuff "python3 aprsbot.py$(printf \\r)"