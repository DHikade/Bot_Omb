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

class Poll(threading.Thread):
    def __init__(self, language, channel, poll_name, poll_options, minute, second):
        self.__language = language.get_Languages()
        threading.Thread.__init__(self)
        self.__start(poll_options)
        self.__poll_name = poll_name
        self.__minute = minute
        self.__second = second
        self.__poll_user_list = {}
        self.__poll_allow = False
        self.__channel = channel
        self.__win_message = ""
        self.__active = True

    def run(self):
        self.__poll_allow = True
        self.__channel.chat(self.__language["poll_start"].format(self.__poll_name, self.__poll_text))
        time.sleep(int(self.__minute)*60 + int(self.__second))
        self.__poll_allow = False
        if self.__active:
            self.__channel.chat(self.__language["poll_finish"].format(self.__poll_name))
            self.__result()

    def __start(self, poll_options):
        poll_options = poll_options[1 : len(poll_options)]
        poll_options_list = []
        poll_text = ""
        for i in range(poll_options.count('/')+1):
            if "/" in poll_options:
                poll_options_list.append({poll_options[0:poll_options.find("/")] : 0})
                poll_text += str(i)+". "+poll_options[0:poll_options.find("/")]
                poll_options = poll_options[poll_options.find("/")+1 : len(poll_options)]
            else:
                poll_options_list.append({poll_options[0:len(poll_options)]: 0})
                poll_text += str(i)+". "+poll_options[0:len(poll_options)]
                poll_options = poll_options[0:len(poll_options)]
        self.__poll_text = poll_text
        self.__poll_option = poll_options_list

    def vote(self, username, poll_vote):
        if self.__poll_allow:
            if not self.__isNumber(poll_vote):
                check = True
                for i in range(len(self.__poll_option)):                    
                    if self.__poll_option[i].keys()[0].lower().replace(" ", "") == poll_vote.lower().replace(" ", ""):
                        poll_vote = i
                        check = False
                        break
                if check:
                    poll_vote = len(self.__poll_option)
            if int(poll_vote) >= 0 and int(poll_vote) < len(self.__poll_option):
                self.__poll_user_list[username] = int(poll_vote)
                return self.__language["poll_vote"]
            else:
                return self.__language["poll_vote_fail"]
        else:
            return self.__language["poll_progress_off"]

    def isActive(self):
        return self.__poll_allow

    def __result(self):
        for user in self.__poll_user_list:
            for vote in self.__poll_option[self.__poll_user_list[user]]:
                self.__poll_option[self.__poll_user_list[user]][vote] += 1
        poll_win = 0
        poll_win_vote = ""
        poll_win_i = -1
        for i in range(len(self.__poll_option)):
            for vote in self.__poll_option[i]:
                if self.__poll_option[i][vote] > poll_win:
                    poll_win_vote = vote
                    poll_win_i = i
        if poll_win_i >= 0:
            self.__win_message = self.__language["poll_vote_win"].format(self.__poll_name, poll_win_vote, self.__poll_option[poll_win_i][poll_win_vote])
        else:
            self.__win_message = self.__language["poll_vote_not"]
        self.__channel.chat(self.__win_message)

    def result(self):
        self.__channel.chat(self.__win_message)

    def __isNumber(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def finish(self):
        self.__active = False