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

from Robbery import Robbery
from Spy import Spy

import random
import threading
import time
import config

class Bank(threading.Thread):

    def __init__(self, channel_name, channel, whisper):
        threading.Thread.__init__(self)
        self.__channel_name = channel_name
        self.__channel = channel
        self.__whisper = whisper
        self.__robbery = None
        self.__spies = []
        self.__spy_attempts = 0
        self.__active = True
        self.__guards = self.__load("guards.csv", "bank/")
        self.__guards_working = random.sample(self.__guards, random.randint(1,3))
        self.__vault = random.randint(100, 500)
        self.__languages = None

    def set_Language(self, language):
        self.__languages = language

    def run(self):
        while self.__active:
            time.sleep(1200)
            self.__guards_working = random.sample(self.__guards, random.randint(1,3))
            self.__vault = random.randint(100, 500)
            self.__robbery.vault(self.__vault)
            self.__robbery.guards(self.__guards_working)
            self.__robbery.spy(self.__spy_attempts)

    def robbery(self, username):
        if self.__robbery is None:
            self.__robbery_start()
        elif not self.__robbery.is_Active():
            self.__robbery_start()
        self.__robbery.robbery(username)

    def __robbery_start(self):
        self.__robbery = Robbery(self.__languages, self.__channel, self.__whisper)
        self.__robbery.vault(self.__vault)
        self.__robbery.guards(self.__guards_working)
        self.__robbery.spy(self.__spy_attempts)
        self.__robbery.setDaemon(True)
        self.__robbery.start()

    def flee(self, username):
        if self.__robbery is not None:
            self.__robbery.flee(username)
        else:
            self.__whisper.whisper(username, self.__languages["lan"]["robbery_not_active"])

    def spy(self, username):
        spy_already_check = False
        for spy in self.__spies:
            if not spy.is_Active():
                self.__spies.remove(spy)
            elif username == spy.get_Username():
                spy_already_check = True
                break
        if not spy_already_check:
            self.__spy_attempts += 1
            thief_spy = Spy(self.__languages, username, self.__channel, self.__whisper, self.__vault, self.__guards_working)
            thief_spy.setDaemon(True)
            thief_spy.start()
            self.__spies.append(thief_spy)
        else:
            self.__whisper.whisper(username, self.__languages["lan"]["spy_in_progress"])

    def protect(self, username):
        print("ToDo")

    def deposit(self, username):
        print("ToDo")

    def withdraw(self, username):
        print("ToDo")

    def guard_add(self, username, message):
        guard_difficulty = message[message.rfind(' ')+1:len(message)]
        message = message[0:message.rfind(' ')]
        guard_name = message[message.rfind(' ')+1:len(message)]
        self.__guards.append([guard_name, guard_difficulty])
        self.__save("guards.csv", self.__guards, "bank/")
        self.__channel.chat(self.__languages["lan"]["guard_add"].format(guard_name, guard_difficulty))

    def guard_remove(self, username, message):
        guard = message[message.rfind(' ')+1:len(message)]
        guard_element = self.__get_element(guard, self.__guards)
        if (len(self.__guards) - 1) < 3:
            self.__whisper.whisper(username, self.__languages["lan"]["guard_remove_fail_count"].format(str(self.__guards)))
        elif guard_element is None:
            self.__whisper.whisper(username, self.__languages["lan"]["guard_remove_fail_list"].format(guard))
        else:
            self.__guards.remove(guard_element)
            self.__whisper.whisper(username, self.__languages["lan"]["guard_remove"].format(str(guard_element)))

    def guard_show(self, message):
        self.__channel.chat(self.__languages["lan"]["guard_show"].format(str(self.__guards)))

    def __get_element(self, key, frm):
        for elem in frm:
            if key in elem:
                return elem
        return None

    def __save(self, file_name, data, sub_folder = ""):
        file_save = open(config.PATH+"channel/"+self.__channel_name+"/"+sub_folder+file_name, 'w')
        for i in range(len(data)):
            output = ''
            for j in range(len(data[i])):
                output += str(data[i][j]) + ";"
            file_save.write(output[:len(output)-1]+"\n")
        file_save.close()

    def __load(self, file_name, sub_folder = ""):
        with open(config.PATH+"channel/"+self.__channel_name+"/"+sub_folder+file_name, 'r') as loaded:
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

    def __update(self, key, data, frm):
        for i in range(len(frm)):
            if key in frm[i]:
                for j in range(len(frm[i])):
                    if data[j] != None:
                        frm[i][j] = data[j]
                return True
        return self.__add(key, data)

    def __string_to_bool(self, message):
        if message == "True":
            return True
        return False

    def __isNumber(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False