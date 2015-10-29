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

import sys
import time

class Bet(object):
    def __init__(self, language):
        self.__language = language.get_Languages()
        self.__bet_time_start = 0
        self.__bet_allow = False
        self.__bets = {}
    
    def start(self):
        if not self.__bet_allow:
            self.__bet_time_start = int(round(time.time()))
            self.__bet_allow = True
            return True
        return False
    
    def stop(self):
        if self.__bet_allow:
            self.__bet_allow = False
            bet_time_end = int(round(time.time())) - self.__bet_time_start
            win_time = sys.maxsize
            win_user = ''
            win_money = 0
            for key in self.__bets:
                if 'bet_spent' in self.__bets[key]:
                    if abs(bet_time_end - self.__bets[key]['bet_time']) < win_time:
                        win_time = abs(bet_time_end - self.__bets[key]['bet_time'])
                        win_user = key
                                    
                    win_fac = (1.0 - abs(((float(bet_time_end))-(float(self.__bets[key]['bet_time'])))/(float(self.__bets[key]['bet_time']))))          
                    if win_fac <= 1:
                        win_money = self.__bets[key]['bet_spent'] + int(win_fac * float(self.__bets[key]['bet_spent']))
                        self.__bets[key]['bet_money'] += win_money
                    else:
                        win_money = 0
            if win_user != '':
                win_money += self.__bets[win_user]['bet_spent']
                self.__bets[win_user]['bet_money'] += win_money
                self.__bet_time_start = 0
                return {"bool" : True, "msg" : self.__language["bet_stop"].format(win_user, str(self.__bets[win_user]['bet_hour']), str(self.__bets[win_user]['bet_min']), str(self.__bets[win_user]['bet_sec']), str(win_money))}
            else:
                return {"bool" : False, "msg" : self.__language["bet_stop_no"]}
        return {"bool" : False, "msg" : self.__language["bet_not_active"]}
    
    def get_bets(self):
        return self.__bets
    
    def reset(self):
        if self.__bet_allow:
            self.__bet_allow = False
            self.__bets = []
            return True
        return False
    
    def bet(self, username, bet_money, bet_spent ,bet_hour, bet_min, bet_sec):
        if self.__bet_allow and (int(round(time.time())) - self.__bet_time_start) < 180:
            if bet_money >= bet_spent:
                bet_money -= bet_spent
                self.__bets[username] = {'bet_money' : bet_money, 'bet_spent' : bet_spent, 'bet_time' : bet_hour*60*60 + bet_min*60 + bet_sec,'bet_hour' : bet_hour, 'bet_min' : bet_min, 'bet_sec' : bet_sec}
                return True
        return False