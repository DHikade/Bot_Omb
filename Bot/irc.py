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

import socket

import config

class irc():
    def __init__(self, host, port, nick, password, channel = None):
        self.__irc_socket = socket.socket()
        self.__irc_host = host
        self.__irc_nick = nick
        self.__irc_password = password
        self.__irc_channel = channel
        self.__irc_channel_active = None
        self.__irc_port = port
        self.__start()

    def __start(self):  
        try:
            self.__connect(self.__irc_host, self.__irc_port)
            self.__login(self.__irc_nick, self.__irc_password)
            if self.__irc_host == config.HOST:
                if self.__irc_channel != None:
                    for i in range(len(self.__irc_channel)):
                        print("IRC: "+self.__irc_channel[i])
                        self.join(self.__irc_channel[i])
                else:
                    print("Connection aboard. No Channel was defined for {0}".format(config.HOST))
                    self.__irc_socket.close()
            elif self.__irc_host == config.HOST_WHISPER_120 or self.__irc_host == config.HOST_WHISPER_119:
                self.__enable_whisper()
            else:
                print("Please check your Host. You can connect to the Twitch IRC Server on {0}. The Group Servers for whispers can be accessed by {1} or {2}".format(config.HOST,config.HOST_WHISPER_120,config.HOST_WHISPER_119))
        except:
            print("Connection to {0} on port {1} failed".format(self.__irc_host, self.__irc_port))

    def getHost(self):
        return self.__irc_host

    def getNick(self):
        return self.__irc_nick

    def getPassword(self):
        return self.__irc_password

    def getChannel(self):
        return self.__irc_channel

    def getPort(self):
        return self.__irc_port

    def switch(self, channel):
        self.__irc_channel_active = channel

    def __login(self, nick, password):
        self.__irc_socket.send("PASS {0}\r\n".format(password).encode("utf-8"))
        self.__irc_socket.send("NICK {0}\r\n".format(nick).encode("utf-8"))

    def join(self, channel):
        self.__irc_socket.send("JOIN {0}\r\n".format(channel).encode("utf-8"))

    def part(self, channel):
        self.__irc_socket.send("PART {0}\r\n".format(channel).encode("utf-8"))

    def __enable_whisper(self):
        self.__irc_socket.send("/CAP REQ :twitch.tv/commands".encode("utf-8"))
        self.__irc_socket.send("/CAP REQ :twitch.tv/tags".encode("utf-8"))

    def quit(self):
        self.__irc_socket.close()

    def __connect(self, host, port):
        self.__irc_socket.connect((host, port))

    def chat(self, message):
        self.__irc_socket.send("PRIVMSG {0} :{1} \r\n".format(self.__irc_channel_active, message).encode("utf-8"))

    def whisper(self, user, message):
        if self.__irc_host == config.HOST_WHISPER_120 or self.__irc_host == config.HOST_WHISPER_119:
            self.__irc_socket.send("PRIVMSG #jtv :/w {0} {1} \r\n".format(user, message).encode("utf-8"))
        else:
            print("You are not connected to the Group Chat Servers! Please connect first to {0} or {1}.".format(config.HOST_WHISPER_120,config.HOST_WHISPER_119))

    def pong(self):
        self.__irc_socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

    def receive(self, bit):
        response = self.__irc_socket.recv(bit).decode("utf-8")
        return response

    def timeout(self, user, secs):
        print("geht das?")
        self.chat(".timeout {0} {1}".format(user, secs))

    def ban(self, user):
        self.chat(".ban {0}".format(user))