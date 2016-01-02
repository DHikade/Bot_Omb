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
import json

class TwitchAPI():
    
    def __init__(self, channel_Nick = None):
        self.__channel_Nick = channel_Nick
        self.__baseKraken = "https://api.twitch.tv/kraken/"
        self.__baseTMI = "https://tmi.twitch.tv/group/user/"

    def setChannel(self, channel_Nick):
        self.__channel_Nick = channel_Nick
    
    def getJSON(self, param):
        try:
            response = urlopen(param)
            str_response = response.read().decode('utf-8')
            api = json.loads(str_response)
        except:
            api = None
        return api
    
    def getKraken_Streams(self):
        return self.getJSON(self.__baseKraken+"streams/"+self.__channel_Nick)
    
    def getKraken_Channels(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick)

    def getKraken_isOnline(self):
        status = self.getJSON(self.__baseKraken+"streams/"+self.__channel_Nick)
        if status is None:
            return False
        elif status['stream'] is None:
            return False
        else:
            return True

    def getKraken_Follows(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/follows")
    
    def getKraken_Follows_List(self):
        follow = []
        json = self.getKraken_Follows()
        while len(json["follows"]) > 0:
            for i in range(len(json["follows"])):
                follow.append(json["follows"][i]["user"]["name"])
            json = self.getJSON(json["_links"]["next"])
        return follow
    
    def getKraken_Follows_Notifications(self):
        follow = []
        json = self.getKraken_Follows()
        while len(json["follows"]) > 0:
            for i in range(len(json["follows"])):
                if json["follows"][i]["notifications"]:
                    follow.append(json["follows"][i]["user"]["name"])
            json = self.getJSON(json["_links"]["next"])
        return follow
    
    def getKraken_Features(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/features") #Brauch Access Token
    
    def getKraken_Subscriptions(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/subscriptions") #Brauch Access Token
    
    def getKraken_Editors(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/editors") #Brauch Access Token
    
    def getKraken_Videos(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/videos")
    
    def getKraken_Videos_List(self):
        video = []
        json = self.getKraken_Videos()
        while len(json["videos"]) > 0:
            for i in range(len(json["videos"])):
                video.append(json["videos"][i]["url"])
            json = self.getJSON(json["_links"]["next"])
        return video
    
    def getKraken_Teams(self):
        return self.getJSON(self.__baseKraken+"channels/"+self.__channel_Nick+"/teams")
    
    def getKraken_Chat(self):
        return self.getJSON(self.__baseKraken+"chat/"+self.__channel_Nick)
    
    def getTMI_Chatters(self):
        return self.getJSON(self.__baseTMI+self.__channel_Nick+"/chatters")
    
    def getTMI_Chatters_Users(self):
        return self.getJSON(self.__baseTMI+self.__channel_Nick+"/chatters")["chatters"]["viewers"]
    
    def getTMI_Chatter_Count(self):
        return self.getJSON(self.__baseTMI+self.__channel_Nick)["chatter_count"]
