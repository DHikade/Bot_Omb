# Bot_Omb

Bot_Omb is a chat moderation bot for Twitch! It is released under the GPLv3 license and is offered as a Software as a Service free of charge. If you want to see Bot_Omb in action, head over to [twitch.tv/Bot_Omb](http://twitch.tv/Bot_Omb)!

For further information about the bot, take a look at the official project page: [Project - Bot_Omb](http://dhika.de/index.php?id=bot_omb)

## Quick and (not so) dirty

If you just want to use the bot, like it is featured in the Repository, you have to visit the production site on [twitch.tv/Bot_Omb](http://twitch.tv/Bot_Omb). There you can tell the bot to join your channel. Just type !follow and thats it...

...ok ok there are some more steps you are now able to do. First of all you should decide if you want to use the bot as moderation supporter or as a feature box. So set your preferences:

!setting warning_url on/off
!setting warning_caps on/off
!setting warning_long_text on/off

If the bot joins your channel for the first time, the preferences are set to off. You should also take a look to the permission levels. For security reasons most of them need a privileges level of 99. To change this behaviour just write !setting command level. You will find a complete list of commands on the production site.

In case you encounter any problem, visit the production site (production site == solution for everything) and type !restart. This will help your bot to help you again!

## Let your Host-System do the work

Feel free and download the bot to use it on your own system but first, let me take you to the following page [twitchapps.com](https://twitchapps.com/tmi/). Here you will get your needed authentication token.
Don't forget to create a new account on Twitch for your bot, and get the authentication token with the new created account!

Now take your config.py and modify it so it fits your needs:

```python
HOST = "irc.twitch.tv"
HOST_WHISPER_120 = "199.9.253.120"
HOST_WHISPER_119 = "199.9.253.119"
PORT = 6667
NICK = "NICK-OF-YOUR-BOT-ACCOUNT"
PASS = "oauth:TWITCHAPP-KEY-OF-YOUR-BOT-ACCOUNT"
RATE = 1.5
VERSION = 1.0
DEVELOPER = "Serdrad0x"
CODE = "Python 3.4"
PATH = "ABSOLUTE-PATH-TO-BOT-FOLDER"
```

Now go to Bot/channel/#bot_omb and open the users.csv. Here you will need to add/modify the following line:

NAME-OF-YOUR-ACCOUNT-LOWERCASE;100;100;False;0;0;0

You need this, to get full permission on the main channel of the bot. Now you are able to start the Main.py in the command line! For further information visit the project page: [Project - Bot_Omb](http://dhika.de/index.php?id=bot_omb)

## Take your (pitch)-fork and contribute

There is a function you totaly need and it isn't implemented already? Don't worry, it is really easy to add new functions!

This is the "brain" of your function. If you need to save any information just add the variable here. It will allow the specific channel to use it in a later state. As a little example you see the poll and bet function, which are special for every channel.

```python
self.__chat_channel[chat_channel[i]] = {
"users" : self.__load("channel/"+chat_channel[i]+"/users.csv"),
"commands" : self.__load("channel/"+chat_channel[i]+"/commands.csv"),
"settings" : self.__load("channel/"+chat_channel[i]+"/settings.csv"),
"bets" : Bet(),
"announcements" : announcements,
"announcelist" : announce,
"smm_submits" : smm_submits,
"poll" : Poll()}
```

To get easy access to the variables, you should asign them to a variable and use them later in the code:

```python
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
elif channel is None:
    print("No channel was found!")
    channel = "Twitch_channel"
```

There are three steps for a good function and every good function got "three" parameters: username, message, privileges. First of all check if the message you receive is the message you need. For this, we use regex!
You can easily add a new regular expression to the regex.py and check it in the Bot_Omb.py. If you want to know if your regex is correct, try [Pythex](http://pythex.org).

A regex could look like this:

```python
REG_HELP_EXTENDED = re.compile('!help[s]{1}[S]*$')
```

The next step is mostly getting user specified information. Most of the time, you only need the privileges level of the user.

```python
user = self.__get_element(username, self.__users)
    if user is not None:
        user_privileges = int(user[eUser.privileges])
    else:
        user_privileges = 0
```

Don't forget to assign default values, if you can't find any. Finally you can start to develop your own function!

```python
def __name(self, username, message, privileges):
    if regex.REG_name.match(message):
        user = self.__get_element(username, self.__users)
        if user is not None:
            user_privileges = int(user[eUser.privileges])
        else:
            user_privileges = 0
        if user_privileges >= privileges:
                ...
        else:
            self.__whisper.whisper(username, "Your privileges level is not high enough to perform this command! You need at least a level of {0}.".format(privileges))
```

Last but not least, you should add a new entry to the settings.csv and add the new function to the list of functions.

```python
if not regex.REG_LOGIN.match(message) and username != 'bot_omb':
    message = message[:len(message)-2]
    print(username + "@" + self.__channel_name + ": " + message)
    self.__warning(username, message)
    self.__command(username, message)
    self.__help(username, message, int(self.__get_element('help', self.__settings)[eSetting.state]))
    self.__coins(username, message, int(self.__get_element('coins', self.__settings)[eSetting.state]))
    ....
```

Everything else you will hopefully learn by reading the code. If not, feel free to ask!