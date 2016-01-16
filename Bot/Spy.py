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

class Spy(threading.Thread):

    def __init__(self, language, username, channel, whisper, vault, guards):
        threading.Thread.__init__(self)
        self.__active = True
        self.__languages = language
        self.__username = username
        self.__channel = channel
        self.__whisper = whisper
        self.__guards = guards
        self.__vault = vault

    def run(self):
        while self.__active:
            spy_time = random.randint(1,120)
            self.__whisper.whisper(self.__username, self.__languages["lan"]["spy_started"].format(str(spy_time)))
            time.sleep(spy_time)
            guards_spied = []
            vault_spied = 0
            for guard in self.__guards:
                if(random.randint(1,100) > int(guard[1])):
                    guards_spied.append(guard)
            if len(guards_spied) == len(self.__guards):
                vault_spied = self.__vault
                self.__whisper.whisper(self.__username, self.__languages["lan"]["spy_perfect"].format(len(self.__guards), str(guards_spied), str(vault_spied)))
            elif len(guards_spied) > 0:
                vault_spied = random.randint(int(self.__vault/10), self.__vault)
                self.__whisper.whisper(self.__username, self.__languages["lan"]["spy_success"].format(len(self.__guards), str(vault_spied)))
            else:
                self.__whisper.whisper(self.__username, self.__languages["lan"]["spy_fail"])
            self.finish()

    def get_Username(self):
        return self.__username

    def set_Language(self, language):
        self.__language = language

    def finish(self):
        self.__active = False

    def is_Active(self):
        return self.__active