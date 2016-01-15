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
import random

class Robbery(threading.Thread):

    def __init__(self, language, channel, whisper):
        threading.Thread.__init__(self)
        self.__languages = language
        self.__channel = channel
        self.__whisper = whisper
        self.__thieves = []
        self.__volatiles = []
        self.__vault = None
        self.__guards = None
        self.__spy_attempts = 0
        self.__active = True
        self.__robbery = False

    def run(self):
        while self.__active:
            self.__robbery = True
            self.__channel.chat(self.__languages["lan"]["robbery_started"])
            time.sleep(180)
            self.__robbery = False
            self.__channel.chat(self.__languages["lan"]["robbery_finished"])
            thieves_caught = []
            for guard in self.__guards:
                thieves_discovered = []
                for thief in self.__thieves:
                    if thief not in thieves_caught:
                        if random.randint(1,100) <= int(guard[1]):
                            thieves_discovered.append(thief)
                for thief in thieves_discovered:
                    if random.randint(1,100) <= int(int(guard[1])/2):
                        thieves_caught.append(thief)
            if len(self.__thieves) == 0:
                self.__channel.chat(self.__languages["lan"]["robbery_cancel"])
            else:
                self.__channel.chat(self.__languages["lan"]["robbery"].format(str(len(thieves_discovered)), str(len(thieves_caught))))
            self.finish()

    def robbery(self, username):
        if username not in self.__thieves:
            if username not in self.__volatiles:
                self.__thieves.append(username)
                self.__whisper.whisper(username, self.__languages["lan"]["robbery_joined"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["robbery_volatile"])
        else:
            self.__whisper.whisper(username, self.__languages["lan"]["robbery_thief"])

    def flee(self, username):
        if self.__robbery:
            chance_to_flee = (len(self.__thieves) - len(self.__volatiles)) * (10 - self.__spy_attempts) 
            if random.randint(1, 100) < chance_to_flee:
                self.__thieves.remove(username)
                self.__volatiles.append(username)
                self.__whisper.whisper(username, self.__languages["lan"]["flee_success"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["flee_fail"])
        else:
            self.__whisper.whisper(username, self.__languages["lan"]["robbery_not_active"])

    def vault(self, money):
        self.__vault = money

    def guards(self, police):
        self.__guards = police

    def spy(self, attempts):
        self.__spy_attempts = attempts

    def finish(self):
        self.__active = False

    def is_Active(self):
        return self.__active
