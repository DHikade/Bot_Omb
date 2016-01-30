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

import threading
import time

class TwitchAPI():

    global follow_counter
    global lock

    lock = threading.Lock()
    follow_counter = {}

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

    def __getKraken_Follows_Notifications_Next_URL(self, username):
        next_url = []
        pages_counter = 0
        json = self.getKraken_Follows()
        follower_amount = int(self.getKraken_Followers())
        page_size = int(follower_amount / 100.0 / 10.0)
        if page_size < 1:
            page_size = 1
        next_url.append(threading.Thread(target=self.__follows_thread_work, args=(username, self.__baseKraken+"channels/"+username+"/follows", page_size,)))
        next_url[len(next_url)-1].start()
        while len(json["follows"]) > 0:
            next_page = json["_links"]["next"]
            next_page = next_page[0:next_page.rfind('=')+1] + "100"
            pages_counter += 1
            if pages_counter == page_size:
                next_url.append(threading.Thread(target=self.__follows_thread_work, args=(username, next_page, page_size,)))
                next_url[len(next_url)-1].start()
                pages_counter = 0
            json = self.__json_receive(next_page)
            if json is None:
                print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Failed to receive JSON from page {0}!".format(str(next_page)))
                break
        return next_url

    def __getKraken_Follows_Notifications_From_Page(self, start_page, pages):
        follow = 0
        json = self.__json_receive(start_page)
        if json is not None:
            for i in range(0, pages):
                for i in range(len(json["follows"])):
                    if json["follows"][i]["notifications"]:
                        follow += 1
                json = self.__json_receive(json["_links"]["next"])
                if json is None:
                    print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Failed to receive JSON from page {0}! Return unfinished follow value of {1}.".format(str(i+1), str(follow)))
                    break
        return follow

    def __json_receive(self, url):
        connection_attempts = 0
        json = self.getJSON(url)
        if json is None:
            while json is None and connection_attempts < 6:
                print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Receiving JSON attempt {0}!".format(str(connection_attempts)))
                json = self.getJSON(url)
                if json is None:
                    connection_attempts += 1
                    time.sleep(10)
            if connection_attempts >= 6:
                return None
            return json
        return json

    def show_follows_thread(self, whisper, username, whisper_name = None):
        global follow_counter
        follow_counter[username] = 0
        print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Generating notific_list for "+username+" request started.")
        notific_list = self.__getKraken_Follows_Notifications_Next_URL(username)
        print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Generating notific_list for "+username+" request finished.")
        print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Counting followers receiving a message for "+username+" started.")
        for thread in notific_list:
            thread.join()
        print(time.strftime("%d.%m.%Y %H:%M:%S") +" - Counting followers receiving a message for "+username+" finished.")
        if whisper_name is None:
            whisper.whisper(username, "{0} of you followers receive a message when your stream starts".format(str(follow_counter[username])))
        else:
            whisper.whisper(whisper_name, "{0} of {1} followers receive a message when the stream starts".format(str(follow_counter[username]), username))
        del follow_counter[username]

    def __follows_thread_work(self, username, start_page, page_size):
        global follow_counter
        count = 0
        count += self.__getKraken_Follows_Notifications_From_Page(start_page, page_size)
        lock.acquire()
        follow_counter[username] += count
        lock.release()

    def getKraken_Followers(self):
        return self.getKraken_Channels()["followers"]

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

    def getKraken_Up_Since(self):
        up_since = self.getKraken_Streams()
        if up_since is not None:
            up_since_stream = up_since["stream"]
            if up_since_stream is not None:
                return up_since_stream["created_at"]
        else:
            return None 

    def getTMI_Chatters(self):
        return self.__json_receive(self.__baseTMI+self.__channel_Nick+"/chatters")

    def getTMI_Chatters_Users(self):
        chatters = self.getTMI_Chatters()
        if chatters is not None:
            return chatters["chatters"]["viewers"]
        else:
            return None

    def getTMI_Chatters_All(self):
        chatters = self.getTMI_Chatters()
        if chatters is not None:
            all_chatters = chatters["chatters"]["moderators"] + chatters["chatters"]["staff"] + chatters["chatters"]["admins"] + chatters["chatters"]["global_mods"] + chatters["chatters"]["viewers"]
            return all_chatters
        else:
            return None

    def getTMI_Chatter_Count(self):
        return self.getJSON(self.__baseTMI+self.__channel_Nick)["chatter_count"]
