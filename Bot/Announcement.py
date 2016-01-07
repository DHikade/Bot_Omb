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

import time
import threading

class Announcement(threading.Thread):
    def __init__(self, ident, message, channel, hour, minute, second):
        threading.Thread.__init__(self)
        self.__ident = ident
        self.__message = message
        self.__channel = channel
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__active = True
    
    def run(self):
        while self.__active:
            time.sleep(self.__hour * 60 * 60 + self.__minute * 60 + self.__second)
            if self.__active:
                self.__channel.chat(self.__message)
            
    def getData(self):
        return self.__ident+";"+self.__hour+";"+self.__minute+";"+self.__second+";"+self.__message+"\n"
    
    def getID(self):
        return self.__ident
    
    def setHour(self, hour):
        self.__hour = hour
        
    def setMinute(self, minute):
        self.__minute = minute
        
    def setSecond(self, second):
        self.__second = second
        
    def setMessage(self, message):
        self.__message = message
        
    def finish(self):
        self.__active = False
