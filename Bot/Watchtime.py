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

from TwitchAPI import TwitchAPI

class Watchtime(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.__users = self.__load("channel/"+name+"/users.csv")
        self.__channel_name = name
        self.__api = TwitchAPI(name.replace("#",""))
        self.__active = True
        self.start()

    def run(self):
        while self.__active:
            time.sleep(60)
            if self.__api.getKraken_isOnline():
                self.__users = self.__load("channel/"+self.__channel_name+"/users.csv")
                if self.__active:
                    users_chat = self.__api.getTMI_Chatters_Users()
                    if users_chat is not None:
                        for i in range(len(users_chat)):
                            user = self.__get_element(users_chat[i].lower(), self.__users)
                            watched = 1
                            if user is not None:
                                watched = int(user[eUser.watchtime]) + 1
                            self.__update(users_chat[i].lower(), [None, None, None, None, None, None, None, watched], self.__users)
                        self.__save("users.csv", self.__users)

    def __watchtime_me(self):
        pass

    def __update(self, key, data, frm):
        for i in range(len(frm)):
            if key in frm[i]:
                for j in range(len(frm[i])):
                    if data[j] != None:
                        frm[i][j] = data[j]
                return True
        return self.__add(key, data)

    def __add(self, key, data):
        if len(data) < 8:
            return False
        for i in range(len(data)):
            if data[i] is None:
                if i is 0:
                    data[i] = key
                elif i is 2:
                    data[i] = 100
                elif i is 3:
                    data[i] = False
                else:
                    data[i] = 0
        data[0] = key
        self.__users.append(data)
        return True

    def __load(self, file_name):
        with open(config.PATH+file_name, 'r') as loaded:
            lines = loaded.readlines()
        loaded_lines = []
        for line in lines:
            entrys = []
            while ';' in line:
                entrys.append(line[:line.find(';')])
                line = line[line.find(';')+1:len(line)]
            entrys.append(line[:len(line)-1])
            loaded_lines.append(entrys)
        return loaded_lines

    def __save(self, file_name, data):
        file_save = open(config.PATH+"channel/"+self.__channel_name+"/"+file_name, 'w')
        for i in range(len(data)):
            output = ''
            for j in range(len(data[i])):
                output += str(data[i][j]) + ";"
            file_save.write(output[:len(output)-1]+"\n")
        file_save.close()

    def __get_element(self, key, frm):
        for elem in frm:
            if key in elem:
                return elem
        return None

    def finish(self):
        self.__active = False