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

import re
import time
import datetime
import copy
import random

import threading

from Bet import Bet
from Announcement import Announcement
from Poll import Poll
from irc import irc
from Greetings import Greetings
from Newtimenowapi import Newtimenowapi
from api import api
from Language import Language
from Bank import Bank
from Watchtime import Watchtime
import eCommand
import eSetting
import eUser
import eAnnouncement
import regex
import config
import data

class Bot_Omb(threading.Thread):
    def __init__(self, chat_channel):
        threading.Thread.__init__(self)
        self.__active = True
        self.__uptime = time.strftime("%d.%m.%Y %H:%M:%S")
        self.__channel_name = ""
        self.__chat_channel = {}
        self.__channel = irc(config.HOST, config.PORT_CHAT, config.NICK, config.PASS, chat_channel)
        self.__whisper = irc(config.HOST, config.PORT_WHISPER, config.NICK, config.PASS)
        for i in range(len(chat_channel)):
            announce = data.load(config.PATH+"channel/"+chat_channel[i]+"/announcements.csv")
            announcements = []
            smm_submits = {}
            for key in announce:
                announcement_thread = Announcement(key[eAnnouncement.ident], key[eAnnouncement.message], self.__channel, int(key[eAnnouncement.hour]), int(key[eAnnouncement.minute]), int(key[eAnnouncement.second]))
                announcement_thread.setName(key[eAnnouncement.ident])
                announcements.append(announcement_thread)
            self.__chat_channel[chat_channel[i]] = {"users" : data.load(config.PATH+"channel/"+chat_channel[i]+"/users.csv"), "commands" : data.load(config.PATH+"channel/"+chat_channel[i]+"/commands.csv"), "settings" : data.load(config.PATH+"channel/"+chat_channel[i]+"/settings.csv"), "ranks" : data.load(config.PATH+"channel/"+chat_channel[i]+"/ranks.csv"), "whitelist" : data.load(config.PATH+"channel/"+chat_channel[i]+"/whitelist.csv"), "quotes" : data.load("channel/"+chat_channel[i]+"/quotes.csv"), "bets" : None, "announcements" : announcements, "announcelist" : announce, "smm_submits" : smm_submits, "poll" : None, "greetings" : None, "language" : None, "bank" : None, "watchtime" : None, "api" : api(chat_channel)}
            self.__chat_channel[chat_channel[i]]["language"] = Language(data.get_element('language_chat', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state])
            self.__chat_channel[chat_channel[i]]["api"].start()
            if data.string_to_bool(data.get_element('bank_mode', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state]):
                self.__chat_channel[chat_channel[i]]["bank"] = Bank(chat_channel[i], self.__channel, self.__whisper)
            if data.string_to_bool(data.get_element('greetings', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state]):
                self.__chat_channel[chat_channel[i]]["greetings"] = Greetings(self.__chat_channel[chat_channel[i]]['api'], self.__chat_channel[chat_channel[i]]['language'], chat_channel[i], self.__channel, data.load(config.PATH+"channel/"+chat_channel[i]+"/greetings.csv"), int(data.get_element('greetings_interval', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state]))
            if data.string_to_bool(data.get_element('announce_mode', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state]):
                for key in announcements:
                    key.start()
            if data.string_to_bool(data.get_element('watchtime_mode', self.__chat_channel[chat_channel[i]]["settings"])[eSetting.state]):
                self.__chat_channel[chat_channel[i]]["watchtime"] = Watchtime(self.__chat_channel[chat_channel[i]]["api"], chat_channel[i], self.__chat_channel[chat_channel[i]]["users"])

    def run(self):
        print("Thread: {0} started".format(self.__chat_channel))
        self.__whisper.whisper('bot_omb', 'Bot activated')
        while self.__active:
            response_channel = self.__channel.receive(1024)
            if response_channel == "PING :tmi.twitch.tv\r\n":
                self.__channel.pong()
                self.__whisper.pong()
            else:
                channel = re.search(r"#\w+", response_channel)
                if channel is not None and channel != self.__chat_channel:
                    channel = channel.group(0)
                    self.__channel_name = channel
                    self.__channel.switch(self.__channel_name)
                    self.__users = self.__chat_channel[self.__channel_name]["users"]
                    self.__commands = self.__chat_channel[self.__channel_name]["commands"]
                    self.__settings = self.__chat_channel[self.__channel_name]["settings"]
                    self.__bets = self.__chat_channel[self.__channel_name]['bets']
                    self.__announcements = self.__chat_channel[self.__channel_name]['announcements']
                    self.__announcelist = self.__chat_channel[self.__channel_name]['announcelist']
                    self.__smm_submits = self.__chat_channel[self.__channel_name]['smm_submits']
                    self.__poll = self.__chat_channel[self.__channel_name]['poll']
                    self.__greetings = self.__chat_channel[self.__channel_name]['greetings']
                    self.__ranks = self.__chat_channel[self.__channel_name]['ranks']
                    self.__bank = self.__chat_channel[self.__channel_name]['bank']
                    self.__whitelist = self.__chat_channel[self.__channel_name]['whitelist']
                    self.__quotes = self.__chat_channel[self.__channel_name]['quotes']
                    self.__languages = {"obj" : self.__chat_channel[self.__channel_name]['language'], "lan" : self.__chat_channel[self.__channel_name]['language'].get_Languages()}
                    self.__api = self.__chat_channel[self.__channel_name]["api"]
                    self.__bank.set_Language(self.__languages)
                elif channel is None:
                    print("No channel was found!")
                    channel = "Twitch_channel"
                    
                username = re.search(r"\w+", response_channel)
                if username is not None:
                    username = username.group(0)
                else:
                    print("No username was found!")
                    username = "Twitch_username"
                
                message = regex.REG_MSG.sub("", response_channel)
                
                if not regex.REG_LOGIN.match(message) and username != 'bot_omb':
                    message = message[:len(message)-2]
                    actual_time = time.strftime("%d.%m.%Y %H:%M:%S")
                    output = actual_time + " - " + username + "@" + self.__channel_name + ": " + message
                    print(output.decode('ascii', 'ignore'))

                    self.__warning(username, message)
                    self.__command(username, message)
                    self.__language(username, message, int(data.get_element('language', self.__settings)[eSetting.state]))
                    self.__upsince(username, message, int(data.get_element('upsince', self.__settings)[eSetting.state]))
                    self.__unfollow(username, message, int(data.get_element('unfollow', self.__settings)[eSetting.state]))
                    self.__info(username, message, int(data.get_element('info', self.__settings)[eSetting.state]))
                    self.__follow(username, message, int(data.get_element('follow', self.__settings)[eSetting.state]))
                    self.__privileges(username, message, int(data.get_element('privileges', self.__settings)[eSetting.state]))
                    self.__setting(username, message, int(data.get_element('setting', self.__settings)[eSetting.state]))
                    self.__setting_show(username, message, int(data.get_element('setting_show', self.__settings)[eSetting.state]))
                    self.__url(username, message, int(data.get_element('url', self.__settings)[eSetting.state]))
                    self.__help(username, message, int(data.get_element('help', self.__settings)[eSetting.state]))
                    self.__coins(username, message, int(data.get_element('coins', self.__settings)[eSetting.state]))
                    self.__clam_ask(username, message, int(data.get_element('clam_ask', self.__settings)[eSetting.state]))
                    self.__roulette(username, message, int(data.get_element('roulette', self.__settings)[eSetting.state]))
                    self.__hug_random(username, message, int(data.get_element('hug_random', self.__settings)[eSetting.state]))
                    self.__hug_other(username, message, int(data.get_element('hug_other', self.__settings)[eSetting.state]))
                    
                    if data.string_to_bool(data.get_element('command_mode', self.__settings)[eSetting.state]):
                        self.__command_add(username, message, int(data.get_element('command_add', self.__settings)[eSetting.state]))
                        self.__command_remove(username, message, int(data.get_element('command_remove', self.__settings)[eSetting.state]))
                        self.__command_show(username, message, int(data.get_element('command_show', self.__settings)[eSetting.state]))
                    
                    if data.string_to_bool(data.get_element('bet_mode', self.__settings)[eSetting.state]):
                        self.__bet_start(username, message, int(data.get_element('bet_start', self.__settings)[eSetting.state]))
                        self.__bet(username, message, int(data.get_element('bet', self.__settings)[eSetting.state]))
                        self.__bet_stop(username, message, int(data.get_element('bet_stop', self.__settings)[eSetting.state]))
                        self.__bet_reset(username, message, int(data.get_element('bet_reset', self.__settings)[eSetting.state]))
                    
                    if data.string_to_bool(data.get_element('follow_mode', self.__settings)[eSetting.state]):
                        self.__follow_member(username, message, int(data.get_element('follow_member', self.__settings)[eSetting.state]))
                        self.__follow_member_other(username, message, int(data.get_element('follow_member_other', self.__settings)[eSetting.state]))
                    
                    if data.string_to_bool(data.get_element('announce_mode', self.__settings)[eSetting.state]):
                        self.__announce_add(username, message, int(data.get_element('announce_add', self.__settings)[eSetting.state]))
                        self.__announce_remove(username, message, int(data.get_element('announce_remove', self.__settings)[eSetting.state]))
                        self.__announce_show(username, message, int(data.get_element('announce_show', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('smm_mode', self.__settings)[eSetting.state]):
                        self.__smm_level_submit(username, message, int(data.get_element('smm_level_submit', self.__settings)[eSetting.state]))
                        self.__smm_level_submit_other(username, message, int(data.get_element('smm_level_submit_other', self.__settings)[eSetting.state]))
                        self.__smm_level_show(username, message, int(data.get_element('smm_level_show', self.__settings)[eSetting.state]))
                        self.__smm_level_next(username, message, int(data.get_element('smm_level_next', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('poll_mode', self.__settings)[eSetting.state]):
                        self.__poll_start(username, message, int(data.get_element('poll_start', self.__settings)[eSetting.state]))
                        self.__poll_vote(username, message, int(data.get_element('poll_vote', self.__settings)[eSetting.state]))
                        self.__poll_vote_hashtag(username, message, int(data.get_element('poll_vote', self.__settings)[eSetting.state]))
                        self.__poll_result(username, message, int(data.get_element('poll_result', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('rank_mode', self.__settings)[eSetting.state]):
                        self.__rank_add(username, message, int(data.get_element('rank_add', self.__settings)[eSetting.state]))
                        self.__rank_remove(username, message, int(data.get_element('rank_remove', self.__settings)[eSetting.state]))
                        self.__rank_show(username, message, int(data.get_element('rank_show', self.__settings)[eSetting.state]))
                        self.__rank_show_me(username, message, int(data.get_element('rank_show_me', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('bank_mode', self.__settings)[eSetting.state]):
                        self.__bank_robbery(username, message, int(data.get_element('bank_robbery', self.__settings)[eSetting.state]))
                        self.__bank_spy(username, message, int(data.get_element('bank_spy', self.__settings)[eSetting.state]))
                        self.__bank_robbery_flee(username, message, int(data.get_element('bank_robbery_flee', self.__settings)[eSetting.state]))
                        self.__bank_guard_add(username, message, int(data.get_element('bank_guard_add', self.__settings)[eSetting.state]))
                        self.__bank_guard_remove(username, message, int(data.get_element('bank_guard_remove', self.__settings)[eSetting.state]))
                        self.__bank_guard_show(username, message, int(data.get_element('bank_guard_show', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('whitelist_mode', self.__settings)[eSetting.state]):
                        self.__whitelist_add(username, message, int(data.get_element('whitelist_add', self.__settings)[eSetting.state]))
                        self.__whitelist_remove(username, message, int(data.get_element('whitelist_remove', self.__settings)[eSetting.state]))
                        self.__whitelist_show(username, message, int(data.get_element('whitelist_show', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('watchtime_mode', self.__settings)[eSetting.state]):
                        self.__watchtime_me(username, message, int(data.get_element('watchtime_me', self.__settings)[eSetting.state]))

                    if data.string_to_bool(data.get_element('quote_mode', self.__settings)[eSetting.state]):
                        self.__quote_add(username, message, int(data.get_element('quote_add', self.__settings)[eSetting.state]))
                        self.__quote_remove(username, message, int(data.get_element('quote_remove', self.__settings)[eSetting.state]))
                        self.__quote_show(username, message, int(data.get_element('quote_show', self.__settings)[eSetting.state]))
                    
                    time.sleep(config.RATE)
        print("Thread: {0} shutdown".format(self.__channel_name))
        
    def get_Channel(self):
        return self.__chat_channel

    def __language(self, username, message, privileges):
        if regex.REG_LANG.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                language = message[message.find(" ")+1 : len(message)]
                if language in self.__languages["obj"].get_Languages_avaiable():
                    self.__languages["obj"].set_Language(language)
                    self.__languages["lan"] = self.__languages["obj"].get_Languages()
                    self.__channel.chat(self.__languages["lan"]["language_switch"].format(self.__languages["obj"].get_Language()))
                    data.update("language_chat", [None, language], self.__settings)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/settings.csv", self.__settings)
                    self.__settings = data.load(config.PATH+"channel/"+self.__channel_name+"/settings.csv")
                    self.__chat_channel[self.__channel_name]["settings"] = self.__settings
                    if self.__bets is not None or self.__greetings is not None or self.__poll is not None:
                        self.__channel.chat(self.__languages["lan"]["language_later"])
                else:
                    self.__channel.chat(self.__languages["lan"]["language_switch_fail"].format(language))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))
    
    def __quote_add(self, username, message, privileges):
        if regex.REG_QUOTE_ADD.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                message = message[message.find(' ')+1:len(message)]
                message = message[message.find(' ')+1:len(message)]
                quote_user = message[0:message.find(' ')]
                message = message[message.find(' ') : len(message)]
                quote_message = message[message.find(' ')+1:len(message)]                
                self.__quotes.append([str(len(self.__quotes)), quote_user, quote_message, str(time.strftime("%d.%m.%Y %H:%M:%S"))])
                data.save("quotes.csv", self.__quotes)
                self.__chat_channel[self.__channel_name]['quotes'] = self.__quotes
                self.__channel.chat(self.__languages["lan"]["quote_add"].format(quote_message, quote_user))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __quote_remove(self, username, message, privileges):
        if regex.REG_QUOTE_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                quote_id = int(message[message.rfind(' ')+1 : len(message)])
                if quote_id < 0 or quote_id >= len(self.__quotes):
                    self.__channel.chat(self.__languages["lan"]["quote_remove_fail"].format(str(quote_id)))
                else:
                    del self.__quotes[quote_id]
                    data.save("quotes.csv", self.__quotes)
                    self.__chat_channel[self.__channel_name]['quotes'] = self.__quotes
                    self.__channel.chat(self.__languages["lan"]["quote_remove_success"].format(str(quote_id)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __quote_show(self, username, message, privileges):
        if message == "!quotes":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if len(self.__quotes) > 0:
                    quote_choice = random.choice(self.__quotes)
                    self.__channel.chat(self.__languages["lan"]["quote_choice"].format(str(quote_choice[0]), str(quote_choice[2]), str(quote_choice[1]), str(quote_choice[3])))
                else:
                    self.__channel.chat(self.__languages["lan"]["quote_choice_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __hug_random(self, username, message, privileges):
        if message == "!hug random":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                all_chatters = self.__api.getChatters(self.__channel_name)
                if all_chatters is not None:
                    all_chatters.remove(username)
                    if len(all_chatters) >= 1:
                        self.__channel.chat(self.__languages["lan"]["hug_person"].format(str(random.choice(all_chatters)), username))
                    else:
                        self.__channel.chat(self.__languages["lan"]["hug_alone"].format(username))
                else:
                    self.__channel.chat(self.__languages["lan"]["hug_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __hug_other(self, username, message, privileges):
        if regex.REG_HUG_OTHER.match(message) and message != "!hug random":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                hug_person = message[message.find(' ')+1:len(message)]
                self.__channel.chat(self.__languages["lan"]["hug_person"].format(hug_person, username))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __watchtime_me(self, username, message, privileges):
        if message == "!watchtime me":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
                user_watchtime = int(user[eUser.watchtime])
            else:
                user_privileges = 0
                user_watchtime = 0
            if user_privileges >= privileges:
                if user_watchtime == 0:
                    self.__channel.chat(self.__languages["lan"]["watchtime_zero"])
                else:
                    user_watchtime_output = data.toTime(user_watchtime)
                    self.__channel.chat(self.__languages["lan"]["watchtime"].format(username, user_watchtime_output[0], user_watchtime_output[1], user_watchtime_output[2]))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __roulette(self, username, message, privileges):
        if message == "!roulette":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if random.randint(1,6) == random.randint(1,6):
                    self.__channel.chat(self.__languages["lan"]["roulette_loose"].format(username))
                    self.__channel.timeout(username, random.randint(1,60))
                else:
                    self.__channel.chat(self.__languages["lan"]["roulette_win"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __clam_ask(self, username, message, privileges):
        if regex.REG_CLAM_ASK.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if random.randint(0,99) <= 49:
                    self.__channel.chat(self.__languages["lan"]["clam_yes"])
                else:
                    self.__channel.chat(self.__languages["lan"]["clam_no"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __whitelist_add(self, username, message, privileges):
        if regex.REG_WHITELIST_ADD.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                name = message[message.rfind(' ')+1:len(message)]
                self.__whitelist.append([name])
                data.save(config.PATH+"channel/"+self.__channel_name+"/whitelist.csv", self.__whitelist)
                self.__whisper.whisper(username, self.__languages["lan"]["whitelist_add"].format(name))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __whitelist_remove(self, username, message, privileges):
        if regex.REG_WHITELIST_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                name = message[message.rfind(' ')+1:len(message)]
                whitelist_elem = data.get_element(name, self.__whitelist)
                if whitelist_elem is not None:
                    self.__whitelist.remove(whitelist_elem)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/whitelist.csv", self.__whitelist)
                    self.__whisper.whisper(username, self.__languages["lan"]["whitelist_remove"].format(name))
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["whitelist_remove_fail"].format(name))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __whitelist_show(self, username, message, privileges):
        if message == "!whitelists":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__channel.chat(self.__languages["lan"]["whitelist_show"].format(str(self.__whitelist)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_robbery(self, username, message, privileges):
        if message == "!bank robbery":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if not self.__bank.isAlive():
                    self.__bank.setDaemon(True)
                    self.__bank.start()
                self.__bank.robbery(username)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_spy(self, username, message, privileges):
        if message == "!bank spy":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if not self.__bank.isAlive():
                    self.__bank.setDaemon(True)
                    self.__bank.start()
                self.__bank.spy(username)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_robbery_flee(self, username, message, privileges):
        if message == "!bank robbery flee":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if not self.__bank.isAlive():
                    self.__bank.setDaemon(True)
                    self.__bank.start()
                self.__bank.flee(username)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_guard_add(self, username, message, privileges):
        if regex.REG_BANK_GUARD_ADD.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__bank.guard_add(username, message)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_guard_remove(self, username, message, privileges):
        if regex.REG_BANK_GUARD_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__bank.guard_remove(username, message)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bank_guard_show(self, username, message, privileges):
        if message == "!bank guards":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__bank.guard_show(message)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __rank_add(self, username, message, privileges):
        if regex.REG_RANK_ADD.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                rank_priv = message[message.rfind(" ")+1 : len(message)]
                message = message[0 : message.rfind(" ")]
                rank_name = message[message.rfind(" ")+1 : len(message)].lower()
                
                if int(rank_priv) >= 0 and int(rank_priv) <= 99:
                    if data.update(rank_name, [None, rank_priv], self.__ranks):
                        self.__channel.chat(self.__languages["lan"]["rank_add_update"].format(rank_name, rank_priv))
                    else:
                        self.__ranks.append([rank_name, rank_priv])
                        output = self.__languages["lan"]["rank_add_append"]
                        output = output.format(rank_name, rank_priv)
                        self.__channel.chat(output)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/ranks.csv", self.__ranks)
                else:
                    self.__channel.chat(self.__languages["lan"]["rank_add_range"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __rank_remove(self, username, message, privileges):
        if regex.REG_RANK_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                rank_name = message[message.rfind(" ")+1 : len(message)]
                rank_elem = data.get_element(rank_name, self.__ranks)
                if rank_elem is not None:
                    self.__ranks.remove(rank_elem)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/ranks.csv", self.__ranks)
                    self.__channel.chat(self.__languages["lan"]["rank_remove"].format(rank_name))
                else:
                    self.__channel.chat(self.__languages["lan"]["rank_remove_fail"].format(rank_name))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __rank_show(self, username, message, privileges):
        if message == "!ranks":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__channel.chat(self.__languages["lan"]["rank_show"].format(str(self.__ranks)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __rank_show_me(self, username, message, privileges):
        if message == "!rank me":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                rank_list = []
                for rank in self.__ranks:
                    if int(rank[1]) == int(user_privileges):
                        rank_list.append(rank[0])
                if len(rank_list) == 0:
                    self.__whisper.whisper(username, self.__languages["lan"]["rank_me_privileges"].format(str(user_privileges)))
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["rank_me"].format(str(rank_list)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __upsince(self, username, message, privileges):
        if message == "!uptime":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                uptime = self.__api.getUpSince(self.__channel_name)
                if uptime is not None:
                    uptime = re.sub('[-:TZ]', '', uptime)
                    up = datetime.datetime.now() - datetime.datetime.strptime(uptime, "%Y%m%d%H%M%S")
                    self.__channel.chat(self.__languages["lan"]["upsince"].format(str(up)[0:str(up).rfind('.')]))
                else:
                    self.__channel.chat(self.__languages["lan"]["upsince_not"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __poll_start(self, username, message, privileges):
        if regex.REG_POLL.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__poll is None or not self.__poll.isActive():
                    poll_name = message[message.find(" ")+1 : message.rfind("(")-1]
                    poll_options = message[message.find("(") : message.rfind(")")]
                    poll_minutes = message[message.rfind(" ")+1 : message.rfind(":")]
                    poll_seconds = message[message.rfind(":")+1 : len(message)]
                    self.__poll = Poll(self.__languages["obj"], self.__channel, poll_name, poll_options, poll_minutes, poll_seconds)
                    self.__chat_channel[self.__channel_name]['poll'] = self.__poll
                    self.__poll.start()
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["poll_progress_on"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __poll_vote(self, username, message, privileges):
        if regex.REG_POLL_VOTE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__poll is not None and self.__poll.isActive():
                    poll_vote = message[message.find(" ")+1 : len(message)]
                    poll_text = self.__poll.vote(username, poll_vote)
                    self.__whisper.whisper(username, poll_text)
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["poll_progress_off"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __poll_vote_hashtag(self, username, message, privileges):
        if regex.REG_POLL_VOTE_HASHTAG.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__poll is not None and self.__poll.isActive():
                    poll_vote = message[1 : len(message)]
                    poll_text = self.__poll.vote(username, poll_vote)
                    self.__whisper.whisper(username, poll_text)
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["poll_progress_off"])
            elif self.__poll.isActive():
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __poll_result(self, username, message, privileges):
        if message == "!result":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__poll is not None:
                    if not self.__poll.isActive():
                        self.__poll.result()
                    else:
                        self.__channel.chat(self.__languages["lan"]["poll_progress"])
                else:
                    self.__channel.chat(self.__languages["lan"]["poll_off"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __smm_level_submit(self, username, message, privileges):
        if regex.REG_SMM_SUBMIT.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                smm_code = message[message.find(' ')+1:len(message)]
                if username in self.__smm_submits:
                    self.__whisper.whisper(username, self.__languages["lan"]["smm_level_switch"].format(self.__smm_submits[username], smm_code))
                    self.__smm_submits[username]["code"] = smm_code
                else:
                    self.__smm_submits[username] = {"user" : username, "code" : smm_code, "id" : time.time()}
                    self.__whisper.whisper(username, self.__languages["lan"]["smm_level_list"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __smm_level_submit_other(self, username, message, privileges):
        if regex.REG_SMM_SUBMIT_OTHER.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                smm_user = message[message.find(' ')+1:message.rfind(' ')].lower()
                smm_code = message[message.rfind(' ')+1:len(message)]
                if smm_user in self.__smm_submits:
                    self.__channel.chat(self.__languages["lan"]["smm_level_switch"].format(self.__smm_submits[smm_user], smm_code))
                    self.__smm_submits[smm_user]["code"] = smm_code
                else:
                    self.__smm_submits[smm_user] = {"user" : smm_user, "code" : smm_code, "id" : time.time()}
                    self.__channel.chat(self.__languages["lan"]["smm_level_list_user"].format(smm_user))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __smm_level_remove(self, username, message, privileges):
        if regex.REG_SMM_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                smm_user = message[message.rfind(' ')+1:len(message)]
                if smm_user in self.__smm_submits:
                    self.__channel.chat(self.__languages["lan"]["smm_level_list_delete"].format(self.__smm_submits[smm_user], smm_user))
                    self.__smm_submits.pop(smm_user, None)
                else:
                    self.__channel.chat(self.__languages["lan"]["smm_level_list_fail"].format(smm_user))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __smm_level_current(self, username, message, privileges):
        if message == "!current":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                ''' ToDo '''
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __smm_level_show(self, username, message, privileges):
        if message == "!levels":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__channel.chat(self.__languages["lan"]["smm_level_list_show"].format(str(self.__sortSMM())))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __sortSMM(self):
        sorted_smm_submits = []
        smm_submits = copy.deepcopy(self.__smm_submits)
        smm_submits_len = len(smm_submits)
        while len(sorted_smm_submits) != smm_submits_len:
            value_high = float("inf")
            user_high = None
            keys = smm_submits.keys()
            for i in range(0, len(keys)) :
                if ((smm_submits[keys[i]]["id"] < value_high) and (keys[i] not in sorted_smm_submits)):
                    value_high = smm_submits[keys[i]]["id"]
                    user_high = keys[i]
            smm_submits[user_high].pop("id", None)
            sorted_smm_submits.append(smm_submits[user_high])
            smm_submits.pop(user_high, None)
        return sorted_smm_submits

    def __sortSMMNext(self):
        return self.__sortSMM()[0]

    def __smm_level_next(self, username, message, privileges):
        if message == "!next":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if len(self.__smm_submits.keys()) >= 1:
                    level = self.__sortSMMNext()
                    self.__smm_submits.pop(level["user"], None)
                    self.__channel.chat(self.__languages["lan"]["smm_level_next"].format(level["user"], level["code"]))
                else:
                    self.__channel.chat(self.__languages["lan"]["smm_level_next_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __setting_show(self, username, message, privileges):
        if message == "!settings":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__whisper.whisper(username, self.__languages["lan"]["setting_show"].format(str(self.__settings)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __announce_show(self, username, message, privileges):
        if message == "!announcements":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__whisper.whisper(username, self.__languages["lan"]["announcement_show"].format(str(self.__announcelist)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __announce_remove(self, username, message, privileges):
        if regex.REG_ANNOUNCE_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                announce = message[message.rfind(' ')+1:len(message)]
                for key in self.__announcelist:
                    if key[eAnnouncement.ident] == announce:
                        self.__announcelist.remove(key)
                        break
                for key in self.__announcements:
                    if key.getID() == announce:
                        key.finish()
                        self.__announcements.remove(key)
                        self.__channel.chat(self.__languages["lan"]["announcement_remove"].format(announce))
                        break
                data.save(config.PATH+"channel/"+self.__channel_name+"/announcements.csv", self.__announcelist)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __announce_add(self, username, message, privileges):
        if re.match('!announce',message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if regex.REG_ANNOUNCE_MIN_SEC.match(message):
                    announce_msg = message[message.find(' ')+1:len(message)]
                    announce_id = announce_msg[:announce_msg.find(' ')]
                    announce_msg = announce_msg[announce_msg.find(' ')+1:len(message)]
                    announce_min = int(announce_msg[:announce_msg.find(':')])
                    announce_msg = announce_msg[announce_msg.find(':')+1:len(message)]
                    announce_sec = int(announce_msg[:announce_msg.find(' ')])
                    announce_msg = announce_msg[announce_msg.find(' ')+1:len(message)]
                    announce_check = data.get_element(announce_id, self.__announcelist)
                    if announce_min >= 1 and len(self.__announcelist) < 3:
                        if  announce_check != None:
                            if data.update(announce_id, [announce_id, 0, announce_min, announce_sec, announce_msg], self.__announcelist):
                                for key in self.__announcements:
                                    if key.getID() == announce_id:
                                        key.setMinute(announce_min)
                                        key.setSecond(announce_sec)
                                        key.setMessage(announce_msg)
                                        data.save(config.PATH+"channel/"+self.__channel_name+"/announcements.csv", self.__announcelist)
                                        break
                        else:
                            announce_announcement = Announcement(announce_id, announce_msg, self.__channel, 0, announce_min, announce_sec)
                            announce_announcement.setName(announce_id)
                            self.__announcements.append(announce_announcement)
                            self.__announcelist.append([announce_id, 0, announce_min, announce_sec, announce_msg])
                            data.save(config.PATH+"channel/"+self.__channel_name+"/announcements.csv", self.__announcelist)
                            announce_announcement.start()
                        self.__channel.chat(self.__languages["lan"]["announcement_add"].format(announce_id))
                    else:
                        self.__channel.chat(self.__languages["lan"]["announcement_fail"])
                elif regex.REG_ANNOUNCE_HOUR_MIN_SEC.match(message):
                    announce_msg = message[message.find(' ')+1:len(message)]
                    announce_id = announce_msg[:announce_msg.find(' ')]
                    announce_msg = announce_msg[announce_msg.find(' ')+1:len(message)]
                    announce_hour = int(announce_msg[:announce_msg.find(':')])
                    announce_msg = announce_msg[announce_msg.find(':')+1:len(message)]
                    announce_min = int(announce_msg[:announce_msg.find(':')])
                    announce_msg = announce_msg[announce_msg.find(':')+1:len(message)]
                    announce_sec = int(announce_msg[:announce_msg.find(' ')])
                    announce_msg = announce_msg[announce_msg.find(' ')+1:len(message)]
                    announce_check = data.get_element(announce_id, self.__announcelist)
                    if announce_min >= 1 and len(self.__announcelist) < 3:
                        if  announce_check != None:
                            if data.update(announce_id, [announce_id, 0, announce_min, announce_sec, announce_msg], self.__announcelist):
                                for key in self.__announcements:
                                    if key.getID() == announce_id:
                                        key.setHour(announce_hour)
                                        key.setMinute(announce_min)
                                        key.setSecond(announce_sec)
                                        key.setMessage(announce_msg)
                                        data.save(config.PATH+"channel/"+self.__channel_name+"/announcements.csv", self.__announcelist)
                                        break
                        else:
                            announce_announcement = Announcement(announce_id, announce_msg, self.__channel, announce_hour, announce_min, announce_sec)
                            announce_announcement.setName(announce_id)
                            self.__announcements.append(announce_announcement)
                            self.__announcelist.append([announce_id, announce_hour, announce_min, announce_sec, announce_msg])
                            data.save(config.PATH+"channel/"+self.__channel_name+"/announcements.csv", self.__announcelist)
                            announce_announcement.start()
                        self.__channel.chat(self.__languages["lan"]["announcement_add"].format(announce_id))
                    else:
                        self.__channel.chat(self.__languages["lan"]["announcement_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def part(self):
        self.__channel.part(self.__channel_name)
        print("The channel was successfully left!")

    def __info(self, username, message, privileges):
        if message == "!info":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__whisper.whisper(username, self.__languages["lan"]["info_show"].format(str(config.VERSION), str(config.DEVELOPER), str(config.CODE), str(self.__uptime)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))     

    def __follow(self, username, message, privileges):
        if message == "!follow":
            self.__whisper.whisper(username, self.__languages["lan"]["follow"].format(username))

    def __follow_member(self, username, message, privileges):
        if message == "!member":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                api = Newtimenowapi(self.__channel_name[1:])
                date = str(api.getNewTimeNow_Follow_Since(username))
                if re.match("Not following...", date):
                    self.__channel.chat(self.__languages["lan"]["follow_member_not"].format(username))
                else:
                    self.__channel.chat(self.__languages["lan"]["follow_member"].format(username, date))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __follow_member_other(self, username, message, privileges):
        if regex.REG_FOLLOW_MEMBER_OTHER.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                name = message[message.find(' ')+1:len(message)]
                api = Newtimenowapi(self.__channel_name[1:])
                date = str(api.getNewTimeNow_Follow_Since(name))
                if re.match("Not following...", date):
                    self.__channel.chat(self.__languages["lan"]["follow_member_not"].format(name))
                else:
                    self.__channel.chat(self.__languages["lan"]["follow_member"].format(name, date))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __unfollow(self, username, message, privileges):
        if message == "!unfollow":
            self.__whisper.whisper(username, self.__languages["lan"]["unfollow"].format(username))

    def __bet_start(self, username, message, privileges):
        if message == "!start":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__bets is None:
                    self.__bets = Bet(self.__languages["obj"])
                    self.__chat_channel[self.__channel_name]['bets'] = self.__bets
                    if self.__bets.start() and self.__bets is not None:
                        self.__channel.chat(self.__languages["lan"]["bet_start_seperator"])
                        time.sleep(config.RATE)
                        self.__channel.chat(self.__languages["lan"]["bet_start"])
                    else:
                        self.__channel.chat(self.__languages["lan"]["bet_start_fail"])
                else:
                    self.__channel.chat(self.__languages["lan"]["bet_start_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bet_stop(self, username, message, privileges):
        if message == "!stop":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                bets_stop = self.__bets.stop()
                if bets_stop["bool"]:
                    for key in self.__bets.get_bets():
                        if not data.update(key, [None, None, self.__bets.get_bets()[key]['bet_money'] - self.__bets.get_bets()[key]['bet_spent'], None, None, None, 0, None], self.__users):
                            self.__users.append([key, 0, self.__bets.get_bets()[key]['bet_money'] - self.__bets.get_bets()[key]['bet_spent'], False, 0, 0, 0, 0])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                    self.__bets = None
                    self.__chat_channel[self.__channel_name]['bets'] = self.__bets
                self.__channel.chat(bets_stop["msg"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bet_reset(self, username, message, privileges):
        if message == "!reset":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                if self.__bets.reset():
                    if not data.update(username, [None, None, None, None, None, None, 0, None], self.__users):
                        self.__users.append([username, 0, 100, False, 0, 0, 0, 0])
                    self.__channel.chat(self.__languages["lan"]["bet_reset"])
                    self.__bets = None
                    self.__chat_channel[self.__channel_name]['bets'] = self.__bets
                else:
                    self.__channel.chat(self.__languages["lan"]["bet_reset_fail"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __bet_same_time(self, username, bet_time):
        for key in self.__bets.get_bets():
            if self.__bets.get_bets()[key]['bet_time'] == bet_time:
                if username == key:
                    return False
                return True

    def __bet(self, username, message, privileges):
        if re.match('!bet',message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
                user_money = int(user[eUser.money])
            else:
                user_privileges = 0
                user_money = 100
            if user_privileges >= privileges:                   
                if regex.REG_BET_MIN_SEC.match(message):
                    bet_spent = int(message[message.rfind(' ')+1:len(message)])
                    if user_money >= bet_spent:
                        bet_hour = 0
                        bet_min = int(message[message.find(' ')+1:message.find(':')])
                        bet_sec = int(message[message.find(':')+1:message.rfind(' ')])
                        if not self.__bet_same_time(username, bet_min*60+bet_sec):
                            if self.__bets.bet(username, user_money, bet_spent, bet_hour, bet_min, bet_sec):
                                if not data.update(username, [None, None, None, None, None, None, bet_spent, None], self.__users):
                                    self.__users.append([username, 0, 100, False, 0, 0, bet_spent, 0])
                                self.__whisper.whisper(username, self.__languages["lan"]["bet_accept"].format(username))
                                data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                        else:
                            self.__whisper.whisper(username, self.__languages["lan"]["bet_same_time"])
                    elif user_money < 1:
                        if not data.update(username, [None, None, 10, None, None, None, None, None], self.__users):
                            self.__users.append([username, 0, 10, False, 0, 0, 0, 0])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                        self.__whisper.whisper(username, self.__languages["lan"]["bet_no_coins"].format(username))
                    else:
                        self.__whisper.whisper(username, self.__languages["lan"]["bet_not_enough"].format(username))
                elif regex.REG_BET_HOUR_MIN_SEC.match(message):
                    bet_spent = int(message[message.rfind(' ')+1:len(message)])
                    if user_money >= bet_spent:
                        bet_hour = int(message[message.find(' ')+1:message.find(':')])
                        bet_min = int(message[message.find(':')+1:message.rfind(':')])
                        bet_sec = int(message[message.rfind(':')+1:message.rfind(' ')])
                        if not self.__bet_same_time(username, bet_min*60+bet_sec):
                            if self.__bets.bet(username, user_money, bet_spent, bet_hour, bet_min, bet_sec):
                                if not data.update(username, [None, None, None, None, None, None, bet_spent, None], self.__users):
                                    self.__users.append([username, 0, 100, False, 0, 0, bet_spent, 0])
                                self.__whisper.whisper(username, self.__languages["lan"]["bet_accept"].format(username))
                                data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                        else:
                            self.__whisper.whisper(username, self.__languages["lan"]["bet_same_time"])
                    elif user_money < 1 and not data.string_to_bool(data.get_element('watchtime_mode', self.__settings)[eSetting.state]):
                        if not data.update(username, [None, None, 10, None, None, None, None, None], self.__users):
                            self.__users.append([username, 0, 10, False, 0, 0, 0, 0])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                        self.__whisper.whisper(username, self.__languages["lan"]["bet_no_coins"].format(username))
                    else:
                        self.__whisper.whisper(username, self.__languages["lan"]["bet_not_enough"].format(username))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __url(self, username, message, privileges):
        if regex.REG_URL.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                url_name = message[message.find(' ')+1: len(message)]
                data.update(url_name, [None, None, None, True, None, None, None, None], self.__users)
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __setting(self, username, message, privileges):
        if regex.REG_SETTING.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                setting_name = message[message.find(' ')+1:message.rfind(' ')]
                if data.get_element(setting_name, self.__settings) is not None:
                    setting_state = message[message.rfind(' ')+1:len(message)]
                    if setting_state == "on" or setting_state == "off":
                        if setting_state == "on":
                            if setting_name == "greetings" and self.__greetings is None:
                                self.__greetings = Greetings(self.__api, self.__languages["obj"], self.__channel_name, self.__channel, data.load(config.PATH+"channel/"+self.__channel_name+"/greetings.csv"), int(data.get_element('greetings_interval', self.__settings)[eSetting.state]))
                                self.__chat_channel[self.__channel_name]['greetings'] = self.__greetings
                            if setting_name == "announce_mode" and not data.string_to_bool(data.get_element('announce_mode', self.__settings)[eSetting.state]):
                                announce = data.load(config.PATH+"channel/"+self.__channel_name+"/announcements.csv")
                                announcements = []
                                for key in announce:
                                    announcement_thread = Announcement(key[eAnnouncement.ident], key[eAnnouncement.message], self.__channel, int(key[eAnnouncement.hour]), int(key[eAnnouncement.minute]), int(key[eAnnouncement.second]))
                                    announcement_thread.setName(key[eAnnouncement.ident])
                                    announcements.append(announcement_thread)
                                self.__announcements = announcements
                                self.__chat_channel[self.__channel_name]['announcements'] = self.__announcements
                                self.__announcelist = announce
                                self.__chat_channel[self.__channel_name]['announcelist'] = self.__announcelist
                                for key in announcements:
                                    key.start()
                            if setting_name == "bank_mode" and not data.string_to_bool(data.get_element('bank_mode', self.__settings)[eSetting.state]): 
                                self.__bank = Bank(self.__channel_name, self.__channel, self.__whisper)
                                self.__chat_channel[self.__channel_name]["bank"] = self.__bank
                            if setting_name == "watchtime_mode" and not data.string_to_bool(data.get_element('watchtime_mode', self.__settings)[eSetting.state]):
                                self.__chat_channel[self.__channel_name]["watchtime"] = Watchtime(self.__api, self.__channel_name, self.__users)
                            data.update(setting_name, [None, True], self.__settings)
                        elif setting_state == "off":
                            if setting_name == "greetings" and self.__greetings is not None:
                                self.__greetings.finish()
                                self.__greetings = None
                                self.__chat_channel[self.__channel_name]['greetings'] = self.__greetings
                            if setting_name == "bet_mode" and self.__bets is not None and data.string_to_bool(data.get_element('bet_mode', self.__settings)[eSetting.state]):
                                self.__bet_reset(username, "!reset")
                                self.__bets = None
                                self.__chat_channel[self.__channel_name]['bets'] = self.__bets
                            if setting_name == "announce_mode" and data.string_to_bool(data.get_element('announce_mode', self.__settings)[eSetting.state]):
                                for key in self.__announcements:
                                    key.finish()
                            if setting_name == "bank_mode" and data.string_to_bool(data.get_element('bank_mode', self.__settings)[eSetting.state]): 
                                self.__bank.finish()
                                self.__bank = None
                                self.__chat_channel[self.__channel_name]["bank"] = None
                            if setting_name == "poll_mode" and data.string_to_bool(data.get_element('poll_mode', self.__settings)[eSetting.state]):
                                self.__poll.finish()
                                self.__poll = None
                                self.__chat_channel[self.__channel_name]['poll'] = self.__poll
                            if setting_name == "watchtime_mode" and data.string_to_bool(data.get_element('watchtime_mode', self.__settings)[eSetting.state]):
                                self.__chat_channel[self.__channel_name]["watchtime"].finish()
                                self.__chat_channel[self.__channel_name]["watchtime"] = None
                            data.update(setting_name, [None, False], self.__settings)
                    elif setting_name != "warning_url" and setting_name != "warning_caps" and setting_name != "warning_long_text" and setting_name != "greetings" and setting_name != "command_mode" and setting_name != "bet_mode" and setting_name != "follow_mode" and setting_name != "announce_mode" and setting_name != "smm_mode" and setting_name != "poll_mode" and setting_name != "rank_mode" and setting_name != "bank_mode" and setting_name != "whitelist_mode":
                        if data.isNumber(setting_state):
                            if int(setting_state) >= 0 and int(setting_state) <= 99:
                                data.update(setting_name, [None, int(setting_state)], self.__settings)
                            else:
                                self.__channel.chat(self.__languages["lan"]["setting_range"].format(setting_name, setting_state))
                    self.__channel.chat(self.__languages["lan"]["setting_change"].format(setting_name, setting_state))
                    data.save(config.PATH+"channel/"+self.__channel_name+"/settings.csv", self.__settings)
                    self.__settings = data.load(config.PATH+"channel/"+self.__channel_name+"/settings.csv")
                    self.__chat_channel[self.__channel_name]["settings"] = self.__settings
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __privileges(self, username, message, privileges):
        if regex.REG_PRIVILEGES.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                priv_name = message[message.find(' ')+1: message.rfind(' ')].lower()
                priv_priv = message[message.rfind(' ')+1:len(message)]
                priv_num = priv_priv
                priv_check = True

                if not data.isNumber(priv_num):
                    priv_elem = data.get_element(priv_priv, self.__ranks)
                    if priv_elem is not None:
                        priv_num = priv_elem[1]
                    else:
                        priv_check = False

                if priv_check:
                    if int(priv_num) > 99 or int(priv_num) < 0:
                        self.__channel.chat(self.__languages["lan"]["privileges_range"])
                    else:
                        if not data.update(priv_name, [None, priv_priv, None, None, None, None, None, None], self.__users):
                            self.__users.append([priv_name, priv_priv, 100, False, 0, 0, 0, 0])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)
                        self.__whisper.whisper(username, self.__languages["lan"]["privileges_assign"].format(priv_name, username, str(priv_priv)))
                        self.__whisper.whisper(priv_name, self.__languages["lan"]["privileges_assign_msg"].format(str(priv_priv)))
                else:
                    self.__whisper.whisper(username, self.__languages["lan"]["privileges_rank_fail"].format(str(priv_priv)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __coins(self, username, message, privileges):
        if message == "!coins":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
                user_coins = int(user[eUser.money])
                user_lock = int(user[eUser.money_lock])
            else:
                user_privileges = 0
                user_coins = 100
                user_lock = 0
            if user_privileges >= privileges:
                self.__whisper.whisper(username, self.__languages["lan"]["coins"].format(user_coins - user_lock))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __command_remove(self, username, message, privileges):
        if regex.REG_COMMAND_REMOVE.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                com = message[message.rfind(' ')+1:len(message)]
                com_elem = data.get_element(com, self.__commands)
                if com_elem != None:
                    self.__commands.remove(com_elem)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/commands.csv", self.__commands)
                    self.__channel.chat(self.__languages["lan"]["command_remove"].format(com))
                else:
                    self.__channel.chat(self.__languages["lan"]["command_remove_fail"].format(com))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __command_add(self, username, message, privileges):
        if regex.REG_COMMAND.match(message):
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                com_message = message[message.find(' ')+1:len(message)]
                com = com_message[:com_message.find(' ')]
                com_element = data.get_element(com, self.__commands)
                com_message = com_message[com_message.find(' ')+1:len(com_message)]
                com_privileges = int(com_message[:com_message.find(' ')])
                com_message = com_message[com_message.find(' ')+1:len(com_message)]
                if  com_element is None:
                    if com_privileges > 99 and com_privileges < 0:
                        self.__whisper.whisper(username, self.__languages["lan"]["command_add_privileges"])
                    else:
                        self.__commands.append([com,str(com_privileges),com_message])
                        data.save(config.PATH+"channel/"+self.__channel_name+"/commands.csv", self.__commands)
                        self.__channel.chat(self.__languages["lan"]["command_add"])
                else:
                    data.update(com, [com, com_privileges, com_message], self.__commands)
                    data.save(config.PATH+"channel/"+self.__channel_name+"/commands.csv", self.__commands)
                    self.__channel.chat(self.__languages["lan"]["command_update"])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __command(self, username, message):
        com = data.get_element(message, self.__commands)
        if com is not None:
            com_privileges = int(com[eCommand.privileges])
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= com_privileges:
                self.__channel.chat(com[eCommand.message])
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(user_privileges))

    def __command_show(self, username, message, privileges):
        if message == "!commands":
            user = data.get_element(username, self.__users)
            if user is not None:
                user_privileges = int(user[eUser.privileges])
            else:
                user_privileges = 0
            if user_privileges >= privileges:
                self.__whisper.whisper(username, self.__languages["lan"]["command_show"].format(str(self.__commands)))
            else:
                self.__whisper.whisper(username, self.__languages["lan"]["privileges_check_fail"].format(privileges))

    def __warning_url(self, username, message):
        if regex.REG_URL_CHECK.match(message):
            setting = data.get_element('warning_url', self.__settings)
            if setting is not None:
                if data.string_to_bool(setting[eSetting.state]):
                    user = data.get_element(username, self.__users)
                    if user is not None:
                        user_permit = data.string_to_bool(user[eUser.url_permit])
                        user_privileges = int(user[eUser.privileges])
                    else:
                        user_permit = False
                        user_privileges = 0
                    if not user_permit and user_privileges < 70:
                        self.__channel.chat(self.__languages["lan"]["warning_url"].format(username))
                        self.__channel.timeout(username, 1)
                        return True
                    else:
                        if not data.update(username, [None, None, None, False, None, None, None, None], self.__users):
                            self.__users.append([username, 0, 100, False, 0, 0, 0, 0])
                        return False
        return False

    def __warning_caps(self, username, message):
        if regex.REG_CAPS.match(message):
            setting = data.get_element('warning_caps', self.__settings)
            if setting is not None:
                if data.string_to_bool(setting[eSetting.state]):
                    user = data.get_element(username, self.__users)
                    if user is not None:
                        user_privileges = int(user[eUser.privileges])
                    else:
                        user_privileges = 0
                    if user_privileges < 70:
                        self.__channel.chat(self.__languages["lan"]["warning_caps"].format(username))
                        self.__channel.timeout(username, 1)
                        return True
        return False

    def __warning_long_text(self, username, message):
        if len(message) > 400:
            setting = data.get_element('warning_long_text', self.__settings)
            if setting is not None:
                if data.string_to_bool(setting[eSetting.state]):
                    user = data.get_element(username, self.__users)
                    if user is not None:
                        user_privileges = int(user[eUser.privileges])
                    else:
                        user_privileges = 0
                    if user_privileges < 70:
                        self.__channel.chat(self.__languages["lan"]["warning_long_text"].format(username))
                        self.__channel.timeout(username, 1)
                        return True
        return False

    def __warning(self, username, message):
        whitelist_user = data.get_element(username, self.__whitelist)
        if whitelist_user is not None:
            if self.__warning_url(username, message) or self.__warning_caps(username, message) or self.__warning_long_text(username, message):
                user = data.get_element(username, self.__users)
                if user is not None:
                    user_warnings = int(user[eUser.warnings])
                    user_warnings_date = int(user[eUser.warnings_date])
                else:
                    user_warnings = 0
                if user_warnings > 0:
                    weeks_since_last_warning = int((int(round(time.time())) - user_warnings_date) / 604800)
                    if user_warnings > weeks_since_last_warning:
                        user_warnings -= (weeks_since_last_warning-1)
                else:
                    user_warnings = 1
                user_warnings_date = int(round(time.time()))
                if not data.update(username, [None, None, None, None, user_warnings, user_warnings_date, None, None], self.__users):
                    self.__users.append([username, 0, 100, False, user_warnings, user_warnings_date, 0, 0])
                data.save(config.PATH+"channel/"+self.__channel_name+"/users.csv", self.__users)

    def __help(self, username, message, privileges):
        if message == '!help':
            self.__whisper.whisper(username, self.__languages["lan"]["help"])
        elif regex.REG_HELP_EXTENDED.match(message):
            help_command = message[message.find(' ')+1:len(message)].replace("\r\n","")
            if help_command[0] == '!':
                help_command = help_command[1:]
            if help_command == "command":
                self.__whisper.whisper(username, self.__languages["lan"]["help_command"])
            elif help_command == "bet":
                self.__whisper.whisper(username, self.__languages["lan"]["help_bet"])
            elif help_command == "start":
                self.__whisper.whisper(username, self.__languages["lan"]["help_start"])
            elif help_command == "stop":
                self.__whisper.whisper(username, self.__languages["lan"]["help_stop"])
            elif help_command == "reset":
                self.__whisper.whisper(username, self.__languages["lan"]["help_reset"])
            elif help_command == "help":
                self.__whisper.whisper(username, self.__languages["lan"]["help_help"])
            elif help_command == "coins":
                self.__whisper.whisper(username, self.__languages["lan"]["help_coins"])
            elif help_command == "url":
                self.__whisper.whisper(username, self.__languages["lan"]["help_url"])
            elif help_command == "priv":
                self.__whisper.whisper(username, self.__languages["lan"]["help_priv"])
            elif help_command == "remove":
                self.__whisper.whisper(username, self.__languages["lan"]["help_remove"])
            elif help_command == "setting":
                self.__whisper.whisper(username, self.__languages["lan"]["help_setting"])
            elif help_command == "follow":
                self.__whisper.whisper(username, self.__languages["lan"]["help_follow"])
            elif help_command == "unfollow":
                self.__whisper.whisper(username, self.__languages["lan"]["help_unfollow"])
            elif help_command == "greetings":
                self.__whisper.whisper(username, self.__languages["lan"]["help_greetings"])
            elif help_command == "poll":
                self.__whisper.whisper(username, self.__languages["lan"]["help_poll"])
            elif help_command == "next":
                self.__whisper.whisper(username, self.__languages["lan"]["help_next"])
            elif help_command == "levels":
                self.__whisper.whisper(username, self.__languages["lan"]["help_levels"])
            elif help_command == "submit":
                self.__whisper.whisper(username, self.__languages["lan"]["help_submit"])

    def finish(self):
        self.__active = False
