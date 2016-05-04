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

from Bot_Omb import Bot_Omb
from irc import irc
from TwitchAPI import TwitchAPI
from Twitter import Twitter
import eUser
import regex
import data

import config
import os
import shutil
import re
import time
import threading

follow_requests = {}

def release(value):
    if hasattr(value, "_tstate_lock"):
        if hasattr(value._tstate_lock, "release"):
            value._tstate_lock.release()

def shutdown(bot_thread):
    bot_thread.part()
    for j in bot_thread.get_Channel():
        if bot_thread.get_Channel()[j]['greetings'] is not None:
            bot_thread.get_Channel()[j]['greetings'].finish()
        if bot_thread.get_Channel()[j]['poll'] is not None:
            bot_thread.get_Channel()[j]['poll'].finish()
        if bot_thread.get_Channel()[j]['watchtime'] is not None:
            bot_thread.get_Channel()[j]['watchtime'].finish()
        if bot_thread.get_Channel()[j]['bank'] is not None:
            bot_thread.get_Channel()[j]['bank'].finish()
        if bot_thread.get_Channel()[j]['api'] is not None:
            bot_thread.get_Channel()[j]['api'].finish()
        for announcement in bot_thread.get_Channel()[j]['announcements']:
            announcement.finish()
    bot_thread.finish()

def follow(username, message, privileges):
    if message == "!follow":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            if not data.has(main_channel_list, "#"+username):
                try:
                    os.mkdir(config.PATH+"channel/"+"#"+username)
                    os.mkdir(config.PATH+"channel/"+"#"+username+"/bank")
                    
                    files = [
                     {"file_name" : "quotes.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : ""},
                     {"file_name" : "guards.csv", "file_path" : config.PATH+"channel/#"+username+"/bank/", "file_data" : "Karl;20\nMark;50\nLisa;40\n"},
                     {"file_name" : "whitelist.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : "bot_omb\nnightbot\ntipeeebot\nwizebot\nmikuia\nmoobot\n"},
                     {"file_name" : "commands.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : ""},
                     {"file_name" : "announcements.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : ""},
                     {"file_name" : "greetings.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : ""},
                     {"file_name" : "settings.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : "language_chat;english\nwarning_url;False\nwarning_caps;False\nwarning_long_text;False\ngreetings;False\ngreetings_interval;60\ncommand_mode;True\nbet_mode;True\nfollow_mode;True\nannounce_mode;True\nsmm_mode;True\npoll_mode;True\nrank_mode;True\nbank_mode;True\nwhitelist_mode;True\nwatchtime_mode;False\nquote_mode;False\nhelp;0\ncoins;0\ncommand_add;99\ncommand_remove;99\ncommand_show;99\nprivileges;99\nsetting;99\nsetting_show;99\nurl;99\nbet;0\nbet_start;99\nbet_stop;99\nbet_reset;99\nfollow;0\nfollow_member;0\nfollow_member_other;99\nunfollow;0\ninfo;0\nannounce_add;99\nannounce_remove;99\nannounce_show;99\nsmm_level_submit;99\nsmm_level_submit_other;99\nsmm_level_show;99\nsmm_level_next;99\npoll_start;99\npoll_vote;99\npoll_result;99\nlanguage;99\nupsince;0\nrank_add;99\nrank_remove;99\nrank_show;99\nrank_show_me;0\nbank_robbery;99\nbank_spy;99\nbank_robbery_flee;99\nbank_guard_add;99\nbank_guard_remove;99\nbank_guard_show;99\nwhitelist_add;99\nwhitelist_remove;99\nwhitelist_show;99\nclam_ask;99\nroulette;99\nwatchtime_me;99\nhug_random;99\nhug_other;99\nquote_add;99\nquote_remove;99\nquote_show;99\n"},
                     {"file_name" : "users.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : username+";100;100;False;0;0;0\n"},
                     {"file_name" : "ranks.csv", "file_path" : config.PATH+"channel/#"+username+"/", "file_data" : ""}
                    ]
                    
                    data.create(files)
                    
                    main_channel_list.append(["#"+username])
                    data.save(config.PATH+"channel/channel.csv", main_channel_list)
                except OSError:
                    main_whisper.whisper(username, "Something went wrong. Please contact a Bot_Omb developer!")
                new_bot_thread = Bot_Omb(["#"+username])
                new_bot_thread.setName("#"+username)
                new_bot_thread.setDaemon(True)
                bot_threads.append(new_bot_thread)
                new_bot_thread.start()
                main_whisper.whisper(username, "I joined your stream! If you want to use my full power, you just need to make me a Mod. Otherwise the auto moderation function will not work.")
            else:
                main_whisper.whisper(username, "I already joined your Chat!")
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges)) 

def unfollow(username, message, privileges):
    if message == "!unfollow":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            if data.has(main_channel_list, "#"+username):
                try:
                    shutil.rmtree(config.PATH+"channel/#"+username)
                    for key in main_channel_list:
                        if key[0] == "#"+username:
                            main_channel_list.remove(key)
                            data.save(config.PATH+"channel/channel.csv", main_channel_list)
                            break
                except OSError:
                    main_whisper.whisper(username, "Something went wrong. Please contact a Bot_Omb developer!")
                for i in range(len(bot_threads)):
                    if "#"+username == bot_threads[i].getName():
                        shutdown(bot_threads[i])
                        break
                main_whisper.whisper(username, "It seems like, it is time to say goodbye!")
            else:
                main_whisper.whisper(username, "First things first. If you want me to unfollow your chat, I have to follow first.")
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))  

def restart(username, message, privileges):
    if message == "!restart":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            for i in range(len(bot_threads)):
                if "#"+username == bot_threads[i].getName():
                    shutdown(bot_threads[i])
                    del bot_threads[i]
                    bot_thread = Bot_Omb(["#"+username])
                    bot_thread.setName("#"+username)
                    bot_threads.append(bot_thread)
                    bot_thread.start()
                    main_whisper.whisper(username, "The Bot was restarted. Bot_Omb should be in your Stream again!")
                else:
                    main_whisper.whisper(user, "The Bot can not be restarted, because Bet_Omb is not following your Stream!")
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def restart_all(username, message, privileges):
    if message == "!restart all":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            for i in range(len(bot_threads)):
                shutdown(bot_threads[i])
                bot_thread = Bot_Omb([bot_threads[i].getName()])
                bot_thread.setName(bot_threads[i].getName())
                bot_threads[i] = bot_thread
                bot_thread.start()
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def shutdown_all(username, message, privileges):
    if message == "!shutdown":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            for i in range(len(bot_threads)):
                shutdown(bot_threads[i])
            main_whisper.whisper(username, "Every channel is shutdown!")
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def show_threads(username, message, privileges):
    if message == "!threads":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            data.show(bot_threads)
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def show_follows(username, message, privileges):
    if message == "!follows":
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            api = TwitchAPI(username)
            aprox_time = int(api.getKraken_Followers() * 0.025)
            main_whisper.whisper(username, "Please be patient, while Bot_Omb is handling your !follows request. It will take approximate "+str(aprox_time)+" seconds.")
            follow_thread = threading.Thread(target=api.show_follows_thread, args=(main_whisper, username,))
            follow_thread.setDaemon(True)
            follow_thread.start()
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def show_follows_other(username, message, privileges):
    if regex.REG_FOLLOWS_OTHER.match(message):
        user = data.get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            check = True
            if username in follow_requests:
                if follow_requests[username].isAlive():
                    check = False
                    main_whisper.whisper(username, "Your request is still in progress, please be patient!")
                else:
                    del follow_requests[username]
            if check:
                follows_name = message[message.find(' ')+1 : len(message)]
                api = TwitchAPI(follows_name)
                aprox_time = int(api.getKraken_Followers() * 0.025)
                main_whisper.whisper(username, "Please be patient, while Bot_Omb is handling your !follows request. It will take approximate "+str(aprox_time)+" seconds.")
                follow_thread = threading.Thread(target=api.show_follows_thread, args=(main_whisper, follows_name, username,))
                follow_requests[username] = follow_thread
                follow_thread.setDaemon(True)
                follow_thread.start()
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

if __name__ == '__main__':
    main_name = "#bot_omb"
    main_channel = irc(config.HOST, config.PORT_CHAT, config.NICK, config.PASS, [main_name])
    main_whisper = irc(config.HOST, config.PORT_WHISPER, config.NICK, config.PASS)
    main_users = data.load(config.PATH+"channel/"+main_name+"/users.csv")
    main_settings = data.load(config.PATH+"channel/"+main_name+"/settings.csv")
    main_commands = data.load(config.PATH+"channel/"+main_name+"/commands.csv")
    main_channel_list = data.load(config.PATH+"channel/channel.csv")
    with open(config.PATH+"channel/channel.csv", 'r') as loaded:
        lines = loaded.readlines()
    bot_threads = []
    for i in range(len(lines)):
        lines[i] = lines[i][:len(lines[i])-1]
        bot_thread = Bot_Omb([lines[i]])
        bot_thread.setName(lines[i].replace("\n",""))
        bot_thread.setDaemon(True)
        bot_threads.append(bot_thread)
        bot_thread.start()
    twitter = Twitter()
    main_whisper.whisper('serdrad0x', 'The Bot was successfully started!')
    while True:
        response_channel = main_channel.receive(1024)
        if response_channel == "PING :tmi.twitch.tv\r\n":
            main_channel.pong()
            main_whisper.pong()
        else:
            username = re.search(r"\w+", response_channel)
            if username is not None:
                username = username.group(0)
            else:
                print("No username message:" + response_channel)
            message = regex.REG_MSG.sub("", response_channel)
            if not regex.REG_LOGIN.match(message) and username != 'bot_omb':
                message = message[:len(message)-2]
                actual_time = time.strftime("%d.%m.%Y %H:%M:%S")
                output = actual_time + " - " + username + "@" + main_name + ": " + message
                print(output.decode('ascii', 'ignore'))

                follow(username, message, 0)
                unfollow(username, message, 0)
                restart(username, message, 0)
                restart_all(username, message, 99)
                show_threads(username, message, 99)
                shutdown_all(username, message, 99)
                show_follows(username, message, 0)
                show_follows_other(username, message, 99)
