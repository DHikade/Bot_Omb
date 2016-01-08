#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This is Bot_Omb, a Twitch-Moderation-Bot written in Python and here
    to help you in any kind of your daily streaming life.
    
    For further information you can visit:
        - http://www.twitch.tv/bot_omb
        - http://dhika.de/index.php?id=bot_omb
        - https://github.com/DHikade/Bot_Omb
        
    Copyright (C) 2015 Dominik Hikade

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses.
    
'''

from TwitchAPI import TwitchAPI
from twython import Twython

import config
import random
import time
import json
import threading

class Twitter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__api_Twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)
        self.__api_Twitch = TwitchAPI()
        self.__channel_status = {}
        self.__status = ["belästigt Leute", "gurkt rum", "langweilt Andere", "vergrault Zuschauer", "präsentiert sich", "sucht den Lichtschalter", "sucht den Sinn des Lebens"]
        self.setDaemon(True)
        self.start()

    def run(self):
        while self.isAlive():
            channels = self.__api_Twitch.getJSON(config.TWITTER)
            
            if channels is not None:
                for channel in channels["stream"]:
                    if channel not in self.__channel_status:
                        self.__channel_status[channel] = False
                    self.__api_Twitch.setChannel(channel)
                
                    if self.__api_Twitch.getKraken_isOnline():
                        if not self.__channel_status[channel]:
                            self.__channel_status[channel] = True
                            output = channel + " " + random.choice(self.__status).decode("utf-8") + " auf Twitch! Schau vorbei unter http://twitch.tv/" + channel
                            self.__api_Twitter.update_status(status=output)
                    else:
                        self.__channel_status[channel] = False
            time.sleep(60)
