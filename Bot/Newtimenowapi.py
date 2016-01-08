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

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

class Newtimenowapi(object):

    def __init__(self, channel_Nick = None):
        self.__channel_Nick = channel_Nick
        self.__baseNewTimeNow = "http://api.newtimenow.com/"

    def getNewTimeNow_Follow_Since(self, username):
        try:
            response = urlopen(self.__baseNewTimeNow+"follow-length/?channel="+self.__channel_Nick+"&user="+username)
            str_response = response.read().decode('utf-8')
        except:
            str_response = "USER"
        return str_response
