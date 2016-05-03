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
import eUser
import config
import data

class Watchtime(threading.Thread):

    def __init__(self, api, name, users):
        threading.Thread.__init__(self)
        self.__users = users
        self.__channel_name = name
        self.__api = api
        self.__active = True
        self.start()
        
    def run(self):
        while self.__active:
            time.sleep(60)
            if self.__api.getOnlineState(self.__channel_name):
                self.__users = data.load(config.PATH+"channel/"+self.__channel_name+"/users.csv")
                if self.__active:
                    users_chat = self.__api.getChatters(self.__channel_name)
                    if users_chat is not None:
                        for i in range(len(users_chat)):
                            user = data.get_element(users_chat[i].lower(), self.__users)
                            if user is not None:
                                watched = int(user[eUser.watchtime]) + 1
                                if not data.update(users_chat[i].lower(), [None, None, None, None, None, None, None, watched], self.__users):
                                    self.__users.append([users_chat[i].lower(), 0, 100, False, 0, 0, 0, watched])
                            else:
                                watched = 1
                                self.__users.append([users_chat[i].lower(), 0, 100, False, 0, 0, 0, watched])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)

    def finish(self):
        self.__active = False