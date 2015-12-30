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
import eUser
import regex

import config
import os
import shutil
import re
import time

def show(elements):
    for i in range(len(elements)):
        print(elements[i])

def get_element(key, frm):
    for elem in frm:
        if key in elem:
            return elem
    return None

def save(file_name, data):
    file_save = open(config.PATH+"channel/"+file_name, 'w')
    for i in range(len(data)):
        output = ''
        for j in range(len(data[i])):
            output += str(data[i][j]) + ";"
        file_save.write(output[:len(output)-1]+"\n")
    file_save.close()

def load(file_name):
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

def has(arr, element):
    for key in arr:
        if key[0] == element:
            return True
    return False

def release(value):
    if hasattr(value, "_tstate_lock"):
        if hasattr(value._tstate_lock, "release"):
            value._tstate_lock.release()

def stop(value):
    if hasattr(value, "_stop()"):
        value._stop()

def shutdown(bot_thread):
    bot_thread.part()
    for j in bot_thread.get_Channel():
        if bot_thread.get_Channel()[j]['greetings'] is not None:
            release(bot_thread.get_Channel()[j]['greetings'])
            stop(bot_thread.get_Channel()[j]['greetings'])
        if bot_thread.get_Channel()[j]['poll'] is not None:
            release(bot_thread.get_Channel()[j]['poll'])
            stop(bot_thread.get_Channel()[j]['poll'])
        for announcement in bot_thread.get_Channel()[j]['announcements']:
            release(announcement)
            stop(announcement)
    release(bot_thread)
    stop(bot_thread)

def follow(username, message, privileges):
    if message == "!follow":
        user = get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            if not has(main_channel_list, "#"+username):
                try:
                    os.mkdir(config.PATH+"channel/"+"#"+username)
                    commands_file = open(config.PATH+"channel/"+"#"+username+"/"+"commands.csv", "w")
                    commands_file.write("")
                    commands_file.close()
                    announce_file = open(config.PATH+"channel/"+"#"+username+"/"+"announcements.csv", "w")
                    announce_file.write("")
                    announce_file.close()
                    greetings_file = open(config.PATH+"channel/"+"#"+username+"/"+"greetings.csv", "w")
                    greetings_file.write("")
                    greetings_file.close()
                    settings_file = open(config.PATH+"channel/"+"#"+username+"/"+"settings.csv", "w")
                    settings_file.write("warning_url;False\nwarning_caps;False\nwarning_long_text;False\ngreetings;False\ngreetings_interval;60\nhelp;0\ncoins;0\ncommand_add;99\ncommand_remove;99\ncommand_show;99\nprivileges;99\nsetting;99\nsetting_show;99\nurl;99\nbet;0\nbet_start;99\nbet_stop;99\nbet_reset;99\nfollow;0\nunfollow;0\ninfo;0\nannounce_add;99\nannounce_remove;99\nannounce_show;99\nsmm_level_submit;99\nsmm_level_submit_other;99\nsmm_level_show;99\nsmm_level_next;99\npoll_start;99\npoll_vote;99\npoll_result;99\nlanguage;99\n")
                    settings_file.close()
                    users_file = open(config.PATH+"channel/"+"#"+username+"/"+"users.csv", "w")
                    users_file.write(username+";100;100;False;0;0;0\n")
                    users_file.close()
                    main_channel_list.append(["#"+username])
                    save("channel.csv", main_channel_list)
                except OSError:
                    main_whisper.whisper(username, "Something went wrong. Please contact a Bot_Omb developer!")
                new_bot_thread = Bot_Omb(["#"+username])
                new_bot_thread.setName("#"+username)
                bot_threads.append(new_bot_thread)
                new_bot_thread.start()
                main_whisper.whisper(username, "I joined your stream! If you want to use my full power, you just need to make me a Mod. Otherwise the auto moderation function will not work.")
            else:
                main_whisper.whisper(username, "I already joined your Chat!")
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges)) 

def unfollow(username, message, privileges):
    if message == "!unfollow":
        user = get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            if has(main_channel_list, "#"+username):
                try:
                    shutil.rmtree(config.PATH+"channel/#"+username)
                    for key in main_channel_list:
                        if key[0] == "#"+username:
                            main_channel_list.remove(key)
                            save("channel.csv", main_channel_list)
                            break
                except OSError:
                    main_whisper.whisper(username, "Something went wrong. Please contact a Bot_Omb developer!")
                main_channel.part("#"+username)
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
        user = get_element(username, main_users)
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
        user = get_element(username, main_users)
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
        user = get_element(username, main_users)
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
        user = get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            show(bot_threads)
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))

def show_follows(username, message, privileges):
    if message == "!follows":
        user = get_element(username, main_users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
            api = TwitchAPI(username)
            notific_list = api.getKraken_Follows_Notifications()
            main_whisper.whisper(username, "{0} of your followers receiving a message when your stream starts".format(len(notific_list)))
        else:
            main_whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.$

if __name__ == '__main__':
    main_name = "#bot_omb"
    main_channel = irc(config.HOST, config.PORT, config.NICK, config.PASS, [main_name])
    main_whisper = irc(config.HOST_WHISPER_120, config.PORT, config.NICK, config.PASS)
    main_users = load("channel/"+main_name+"/users.csv")
    main_settings = load("channel/"+main_name+"/settings.csv")
    main_commands = load("channel/"+main_name+"/commands.csv")
    main_channel_list = load("channel/channel.csv")
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
                print(actual_time + " - " + username + "@" + main_name + ": " + message)
                follow(username, message, 0)
                unfollow(username, message, 0)
                restart(username, message, 0)
                restart_all(username, message, 99)
                show_threads(username, message, 99)
                shutdown_all(username, message, 99)
                show_follows(username, message, 99)
