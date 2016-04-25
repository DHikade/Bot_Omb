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

import config
import data

class Greetings(threading.Thread):

    def __init__(self, api, language, name, channel, greeted, interval = 60):
        self.__language = language.get_Languages()
        threading.Thread.__init__(self)
        self.__greeted = greeted
        self.__channel = channel
        self.__interval = interval
        self.__name = name
        self.__api = api
        self.__active = True
        self.start()

    def __greet(self, users):
        usernames = ""
        for i in range(len(users)):
            if i == 0:
                usernames += users[i]
            else:
                usernames += ", " + users[i]
            self.__greeted.append([users[i]])
        data.save(config.PATH+"channel/"+self.__name+"/greetings.csv", self.__greeted)
        self.__channel.chat(self.__language["greetings"].format(usernames))

    def run(self):
        while self.__active:
            time.sleep(self.__interval)
            if self.__api.getOnlineState(self.__name):
                if self.__active:
                    users = self.__api.getUsers(self.__name)
                    if users is not None:
                        greet = []
                        for i in range(len(users)):
                            if [users[i]] not in self.__greeted:
                                greet.append(users[i])
                        if len(greet) > 0:
                            self.__greet(greet)

    def finish(self):
        self.__active = False
