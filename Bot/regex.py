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

REG_CAPS = re.compile('.*[[A-Z\s]{8}]*')
REG_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
REG_LOGIN = re.compile(':.*\.?tmi\.twitch\.tv[\s]{1}')
REG_PRIVILEGES = re.compile('!priv[\s]{1}.+[\S]$')
REG_URL = re.compile('!url[\s]{1}.+[^\s]$')
REG_COMMAND = re.compile('!command[\s]{1}![\S]+[\s]{1}(\d|\d\d)[\s]{1}[\S]+$')
REG_COMMAND_REMOVE = re.compile('!remove[\s]{1}command[\s]{1}![^\s]+$')
REG_BET_MIN_SEC = re.compile('!bet[\s]{1}[0-5]?[0-9]:[0-5][0-9][\s]{1}[0-9]+$')
REG_BET_HOUR_MIN_SEC = re.compile('!bet[\s]{1}(([0-1]?[0-9]|[2][0-3]):)?[0-5][0-9]:[0-5][0-9][\s]{1}[0-9]+$')
REG_ANNOUNCE_MIN_SEC = re.compile('!announce[\s]{1}[\S]+[\s]{1}[0-5]?[0-9]:[0-5][0-9][\s]{1}')
REG_ANNOUNCE_HOUR_MIN_SEC = re.compile('!announce[\s]{1}[\S]+[\s]{1}(([0-1]?[0-9]|[2][0-3]):)?[0-5][0-9]:[0-5][0-9][\s]{1}')
REG_ANNOUNCE_REMOVE = re.compile('!remove[\s]{1}announce[\s]{1}[\S]+')
# PYTHON PORT (Modified) (cc @brifordwylie)
# The $ at the end was removed
# ^(?:(?:https?|ftp)://)? the last ? was added
# (?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})   IP Resolving removed
REG_URL_CHECK = re.compile("^(?:(?:https?|ftp)://)?(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/\S*)?", re.UNICODE)
REG_LANG = re.compile('!lang[\s]{1}[a-z]+$')
REG_HELP = re.compile('!help.*')
REG_HELP_EXTENDED = re.compile('!help[\s]{1}[\S]*$')
REG_AUTO_MOD = re.compile('!automod[\s]{1}(on|off)$')
REG_TICKET = re.compile('!ticket[\s]{1}[\S].*\r\n$')
REG_SETTING = re.compile('!setting[\s]{1}[\S]*[\s]{1}((on|off)|\d\d?)$')
REG_SMM_SUBMIT = re.compile('!submit[\s]{1}([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{4}$')
REG_SMM_SUBMIT_OTHER = re.compile('!submit[\s]{1}[\S]+[\s]{1}([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{4}$')
REG_SMM_REMOVE = re.compile('!remove[\s]{1}level[\s]{1}[\S]+')
REG_POLL = re.compile('!poll[\s]{1}.+[\s]{1}\(.+\)[\s]{1}[0-5]?[0-9]:[0-5][0-9]$')
REG_POLL_VOTE = re.compile('!vote[\s]{1}[0-9]+')
REG_POLL_VOTE_HASHTAG = re.compile('#.*[\S]+$')
REG_FOLLOW_MEMBER_OTHER = re.compile('!member[\s]{1}[\S]+$')
REG_RANK_ADD = re.compile('!rank[\s]{1}add[\s]{1}[\S]*[\s]{1}(\d$|\d\d$)')
REG_RANK_REMOVE = re.compile('!rank[\s]{1}remove[\s]{1}[\S]*$')
REG_FOLLOWS_OTHER = re.compile('!follows[\s]{1}[\S]+$')
REG_BANK_GUARD_REMOVE = re.compile('!bank[\s]{1}guard[\s]{1}remove[\s]{1}[\S]+$')
REG_BANK_GUARD_ADD = re.compile('!bank[\s]{1}guard[\s]{1}add[\s]{1}[\S]+[\s]{1}(\d$|\d\d$)')
REG_WHITELIST_ADD = re.compile('!whitelist[\s]{1}add[\s]{1}[\S]*$')
REG_WHITELIST_REMOVE = re.compile('!whitelist[\s]{1}remove[\s]{1}[\S]*$')
