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

import threading
import time

from TwitchAPI import TwitchAPI

class api(threading.Thread):
    
    def __init__(self, channels):
        threading.Thread.__init__(self)
        self.__twitchapi = TwitchAPI()
        self.__channels = channels
        self.__channel = {}
        self.__active = True
        
    def run(self):
        while self.__active:
            for i in range(len(self.__channels)):
                request = self.__channels[i]
                self.__twitchapi.setChannel(request[1:])
                self.__channel[request] = {
                    "Online" : self.__twitchapi.getKraken_isOnline(), 
                    "UpSince" : self.__twitchapi.getKraken_Up_Since(), 
                    "Chatters" : self.__twitchapi.getTMI_Chatters_All(),
                    "Users" : self.__twitchapi.getTMI_Chatters_Users()
                }
            time.sleep(300)
            
    def getOnlineState(self, channel):
        return self.__channel[channel]["Online"]
    
    def getChatters(self, channel):
        return self.__channel[channel]["Chatters"]
    
    def getUsers(self, channel):
        return self.__channel[channel]["Users"]
    
    def getUpSince(self, channel):
        return self.__channel[channel]["UpSince"]

    def finish(self):
        self.__active = False