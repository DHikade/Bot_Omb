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

class Poll():
    def __init__(self):
        self.__poll_allow = False
        
    def start(self, poll_name, poll_option, minute, second):
        if not self.__poll_allow:
            poll_option = poll_option[1 : len(poll_option)]
            self.__poll_option = []
            poll_text = ""
            for i in range(poll_option.count('/')+1):
                if "/" in poll_option:
                    self.__poll_option.append({poll_option[0:poll_option.find("/")] : 0})
                    poll_text += str(i)+". "+poll_option[0:poll_option.find("/")]
                    poll_option = poll_option[poll_option.find("/")+1 : len(poll_option)]
                else:
                    self.__poll_option.append({poll_option[0:len(poll_option)]: 0})
                    poll_text += str(i)+". "+poll_option[0:len(poll_option)]
                    poll_option = poll_option[0:len(poll_option)]
            self.__poll_name = poll_name
            self.__minute = minute
            self.__second = second
            self.__poll_time_start = int(round(time.time()))
            self.__poll_allow = True
            self.__poll_user_list = {}
            return "The Poll "+ poll_name +" started: "+poll_text
        else:
            return "Poll is already in progress, please wait " + str(int(round(time.time())) - self.__poll_time_start) + "more seconds to start a new one!"
        
    def vote(self, username, poll_vote):
        if self.__poll_allow and (int(round(time.time())) - self.__poll_time_start) < (int(self.__minute)*60 + int(self.__second)):
            if int(poll_vote) < len(self.__poll_option):
                self.__poll_user_list[username] = int(poll_vote)
                return "Your vote was successfully adopted!"
            else:
                return "You voted for a option which is actually not on the list."
        else:
            self.__poll_allow = False
            return "No polls in progress right now!"

    def result(self):
        for user in self.__poll_user_list:
            for vote in self.__poll_option[self.__poll_user_list[user]]:
                self.__poll_option[self.__poll_user_list[user]][vote] += 1
        poll_win = -1
        poll_win_vote = ""
        for i in range(len(self.__poll_option)):
            for vote in self.__poll_option[i]:
                if self.__poll_option[i][vote] > poll_win:
                    poll_win_vote = vote
                    poll_win_i = i
        return "Winner of the poll {0} is {1} with {2} votes!".format(self.__poll_name, poll_win_vote, self.__poll_option[poll_win_i][poll_win_vote])