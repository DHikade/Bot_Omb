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

class Language(object):

    def __init__(self, language = "english"):
        self.__language = language
        self.__languages = {}
        self.__languages_avaiable = ["english", "german"]
        self.set_Language(language)

    def get_Languages_avaiable(self):
        return self.__languages_avaiable

    def get_Language(self):
        return self.__language

    def get_Languages(self):
        return self.__languages

    def set_Language(self, language):
        if language == "english":
            self.__language = language
            self.__languages = {
                "language_switch" : "The language was changed to {0}",
                "language_switch_fail" : "Language could not be changed because {0} was not found!",
                "language_later" : "A module is in progress! The language for the module will be changed after it is finished.",
                "privileges_check_fail" : "Your privileges level is not high enough to perform this command! You need at least a level of {0}.",
                "poll_progress_on" : "Poll is already in progress, please wait until this one is finished!",
                "poll_progress_off" : "No polls in progress right now!",
                "poll_progress" : "Poll still in progress!",
                "poll_off" : "No polls so far!",
                "poll_vote" : "Your vote was successfully adopted!",
                "poll_vote_fail" : "You voted for a option which is actually not on the list.",
                "poll_vote_win" : "Winner of the poll {0} is {1} with {2} votes!",
                "poll_vote_not" : "No one voted for this poll!",
                "poll_start" : "The Poll {0} started: {1}",
                "poll_finish" : "The Poll {0} is finished!",
                "greetings" : "Hi to all new first time Viewers: {0} I hope you enjoy my Stream!",
                "smm_level_list" : "Your Super-Mario-Maker-Level-Code was successfully added to the list. Please be patient while waiting for your Level!",
                "smm_level_switch" : "Your old Level code {0} was exchanged with the new one {1}",
                "smm_level_list_user" : "{0} Super-Mario-Maker-Level-Code was successfully added to the list. Please be patient while waiting for your Level!",
                "smm_level_list_delete" : "The Level {0} from {1} was deleted from the list",
                "smm_level_list_fail" : "No Level found with the id {0}",
                "smm_level_list_show" : "Following Levels are on the list: {0}",
                "smm_level_next" : "The next level we play is from {0} with the code {1}",
                "smm_level_next_fail" : "Sorry, every Level on the List was played!",
                "setting_show" : "These are the channel settings and their states: {0}",
                "announcement_show" : "These are the channel announcements and their settings: {0}",
                "announcement_remove" : "The announcement {0} was successfully removed from the channel!",
                "announcement_add" : "The announcement {0} was successfully added to the channel!",
                "info_show" : "I am Bot_Omb, running in version {0}. My developer is {1} and my source code is written in {2}. I am now up since {3}.",
                "follow" : "Hey {0}, if you want me to join your Stream, just visit my Channel and type there !follow.",
                "unfollow" : "Hey {0}, if you want me to leave your Stream, just visit my Channel and type there !unfollow.",
                "bet_start_seperator" : "##### The run started #####",
                "bet_start" : "You are allowed to bet in the range of three minutes for the actual run. To do so, just write: !bet hh:mm:ss money",
                "bet_start_fail" : "Bet is already in progress, wait until it is finished.",
                "bet_stop" : "The winner is {0}, with a predicted time of {1}:{2}:{3}. You have earned {4} coins.",
                "bet_stop_no" : "Sadly no one bet.",
                "bet_not_active" : "There is no bet in progress!",
                "bet_reset" : "The run was reseted!",
                "bet_reset_fail" : "There is no run which can be reseted",
                "bet_accept" : "Your bet has been successfully adopted {0}",
                "bet_same_time" : "An other User already bet on this time!",
                "bet_no_coins" : "Not even a coin has remained thee {0}. Here is a small financial injection! You got 10 coins.",
                "bet_not_enough" : "{0} you do not have enough money to bet!",
                "setting_range" : "The settings for {0} can only be in the range of 0 to 99",
                "setting_change" : "The settings for {0} was changed to {1}",
                "privileges_range" : "Attention! Privileges can only awarded in the range of 0 to 99!",
                "privileges_assign" : "The user {0} has been assigned by {1} the following authorization: {2}",
                "privileges_assign_msg" : "You got the the following authorization: {0}",
                "coins" : "You got {0} coins",
                "command_remove" : "The command {0} was successfully removed from the chat!",
                "command_remove_fail" : "The command {0} is not set and can not be removed!",
                "command_add_privileges" : "Privileges for commands are only allowed in range of 0 and 99!",
                "command_add" : "Command was successfully added to the chat!",
                "command_update" : "Command was successfully updated!",
                "command_show" : "These are the channel commands and their message: {0}",
                "warning_url" : "Please do not write any URL without permission {0}.",
                "warning_caps" : "{0} seems the Caps lock key to please pretty <3",
                "warning_long_text" : "{0} seems to like very long messages. You should write a PN via Twitch instead!",
                "help" : "What do you want to know? Just type !help <command> for more information.",
                "help_command" : "You can add a new custom command with !command new_command privileges text. For example: !command !test 0 You got it!",
                "help_bet" : "If a run is started, you have the ability to bet. To do so just write !bet hh:mm:ss money. For example: !bet 0:01:23 10. If you never bet before, you start with 100 coins!",
                "help_start" : "Starts a new run and enables the ability to bet on it!",
                "help_stop" : "Stops a run and everyone who bet get an amount of the spent money back. The amount depends on the range to the final time.",
                "help_reset" : "Resets a run and everyone gets the money which was bet back.",
                "help_help" : "This is the help. Here you find every information about the commands you need to know. For example: !help help",
                "help_coins" : "Shows the amount of money you have.",
                "help_url" : "Permits a user to post an URL. For example: !url username",
                "help_priv" : "To perform an action with the bot, you need a special privileges level. With the command !priv level username, you can set the priv of an user. For example: !priv 42 serdrad0x",
                "help_remove" : "You can remove a custom command by writing !remove command. For example: !remove !test",
                "help_setting" : "You can change the settings of the auto moderation if you type !setting warning_url/warning_caps on/off.",
                "help_follow" : "If you want, the bot can follow you to your chat and help to moderate everything. For further information take a look at the Bot_Omb channel.",
                "help_unfollow" : "If you use the Bot_Omb in your chat and don't want it anymore, you can remove it with !unfollow. For further information take a look at the Bot_Omb channel.",
                "help_greetings" : "Every x seconds the bot will check for new users in your channel and look up if they were already greeted. To change this behaviour use !setting greetings on/of and !setting greetings_interval 60",
                "help_poll" : "If you type !poll pollname (optionA / optionB) mm:ss you can start a new poll which will accept votes until time ends. !result shows you the results and !vote num is for voting!",
                "help_next" : "Announces the next Level of the Super Mario Maker - Level - List.",
                "help_levels" : "Shows all level which are added to the Super Mario Maker - Level - List.",
                "help_submit" : "Add a level to the Super Mario Maker - Level - List. You can add a foreign level by typing !submit username levelcode."
            }
            
        if language == "german":
            self.__language = language
            self.__languages = {
                "language_switch" : "Die Sprache wurde geändert zu {0}",
                "language_switch_fail" : "Die Sprache konnte nicht geändert werden da {0} nicht gefunden wurde!",
                "language_later" : "Ein Modul läuft gerade! Die Sprache dieses Moduls wird geändert, sobald es fertig ist.",
                "privileges_check_fail" : "Dein Berechtigungslevel ist nicht hoch genug um das Kommando auszuführen! Du brauchst mindestens ein Berechtigungslevel von {0}.",
                "poll_progress_on" : "Eine Umfrage ist bereits im Gange, bitte warte bis diese vorbei ist!",
                "poll_progress_off" : "Aktuell gibt es keine Umfrage!",
                "poll_progress" : "Eine Umfrage läuft gerade!",
                "poll_off" : "Zur Zeit gibt es keine Umfragen!",
                "poll_vote" : "Deine Abstimmung wurde erfolgreich angenommen!",
                "poll_vote_fail" : "Du hast für eine Option gestimmt, die momentan nicht in der Liste steht.",
                "poll_vote_win" : "Gewinnder der Umfrage {0} ist {1} mit {2} stimmen!",
                "poll_vote_not" : "Niemand hat an der Umfrage teilgenommen!",
                "poll_start" : "Die Umfrage {0} wurde gestartet: {1}",
                "poll_finish" : "Die Umfrage {0} ist beendet!",
                "greetings" : "Hallo an alle die zum ersten Mal zuschauen: {0} Ich hoffe euch gefällt mein Stream!",
                "smm_level_list" : "Dein Super-Mario-Maker-Level-Code wurde erfolgreich zur Liste hinzugefügt. Bitte bewahre ruhe, während du auf dein Level wartest!",
                "smm_level_switch" : "Dein alter Levelcode {0} wurde mit dem Neuen getauscht {1}",
                "smm_level_list_user" : "{0} Super-Mario-Maker-Level-Code wurde erfolgreich zur Liste hinzugefügt. Bitte bewahre ruhe, während du auf dein Level wartest!",
                "smm_level_list_delete" : "Das Level {0} von {1} wurde von der Liste entfernt",
                "smm_level_list_fail" : "Es wurde kein Level gefunden mit der ID {0}",
                "smm_level_list_show" : "Folgende Level befinden sich auf der Liste: {0}",
                "smm_level_next" : "Das nächste Level welches wir spielen ist von {0} und hat den Code {1}",
                "smm_level_next_fail" : "Entschuldigung, jedes Level auf der Liste wurde gespielt!",
                "setting_show" : "Dies sind die Einstellungen des Channels und deren Werte: {0}",
                "announcement_show" : "Dies sind die Ankündigungen des Channels und deren Werte: {0}",
                "announcement_remove" : "Die Ankündigung {0} wurde erfolgreich vom Channel entfernt!",
                "announcement_add" : "Die Ankündigung {0} wurde dem Channel erfolgreich hinzugefügt!",
                "info_show" : "Ich bin Bot_Omb und laufe in Version {0}. Mein Entwickler ist {1} und mein Sourcecode ist geschrieben in {2}. Ich bin aktiv seit {3}.",
                "follow" : "Hey {0}, wenn du möchtest das ich deinem Stream beitrete, besuche doch einfach meinen Channel und schreibe !follow.",
                "unfollow" : "Hey {0}, wenn du möchtest das ich deinen Stream verlasse, besuche doch einfach meinen Channel und schreibe !unfollow.",
                "bet_start_seperator" : "##### Das Rennen startet #####",
                "bet_start" : "Du kannst nun im Zeitraum von drei Minuten für das aktuelle Rennen wetten. Um dies zu tun, schreibe einfach: !bet hh:mm:ss money",
                "bet_start_fail" : "Eine Wette läuft gerade, warte bis es fertig ist.",
                "bet_stop" : "Der Gewinner ist {0}, mit einer geschätzten Zeit von {1}:{2}:{3}. Du erhälst {4} Münzen.",
                "bet_stop_no" : "Traurigerweise hat niemand gewettet.",
                "bet_not_active" : "Aktuell läuft keine Wette!",
                "bet_reset" : "Das Rennen wurde zurückgesetzt!",
                "bet_reset_fail" : "Es gibt kein Rennen welches zurückgesetzt werden könnte",
                "bet_accept" : "Deine Wette wurde erfolgreich angenommen {0}",
                "bet_same_time" : "Jemand anderes hat bereits auf diese Zeit gewettet!",
                "bet_no_coins" : "Nicht mal eine Münze ist dir geblieben {0}. Hier eine kleine finanzielle Spritze! Du bekommst 10 Münzen.",
                "bet_not_enough" : "{0} du hast nicht genug Münzen zum Wetten!",
                "setting_range" : "Die Einstellungen für {0} dürfen sich nur im Bereich von 0 bis 99 bewegen",
                "setting_change" : "Die Einstellungen für {0} wurden geändert zu {1}",
                "privileges_range" : "Achtung! Befugnislevel können nur im Bereich von 0 bis 99 vergeben werden!",
                "privileges_assign" : "Dem Nutzer {0} wurde von {1} die folgende Berechtigung zugewiesen: {2}",
                "privileges_assign_msg" : "Du hast die folgende Berechtigung erhalten: {0}",
                "coins" : "Du hast {0} Münzen",
                "command_remove" : "Das Kommando {0} wurde erfolgreich vom Channel entfernt!",
                "command_remove_fail" : "Das Kommando {0} wurde nicht gesetzt und kann daher nicht entfernt werden!",
                "command_add_privileges" : "Befugnislevel für Kommandos dürfen sich nur im Bereich von 0 bis 99 bewegen!",
                "command_add" : "Das Kommando wurde erfolgreich dem Chat hinzugefügt!",
                "command_update" : "Das Kommando wurde erfolgreich aktualisiert!",
                "command_show" : "Dies sind die Kommandos der Channel und ihre Nachrichten: {0}",
                "warning_url" : "Bitte schreibe keine URL ohne Erlaubnis {0}.",
                "warning_caps" : "{0} scheint die Capslock Taste ziemlich zu mögen <3",
                "warning_long_text" : "{0} scheint sehr lange Nachrichten zu mögen. Du solltest alternativ eine PN über Twitch versenden!",
                "help" : "Was möchtest du wissen? Schreibe einfach !help <command> für weitere Informationen.",
                "help_command" : "Du kannst eigene Kommandos hinzufügen mit !command new_command privileges text. Als Beispiel: !command !test 0 You got it!",
                "help_bet" : "Wenn ein Rennen gestartet wurde, hast du die Möglichkeit zu wetten. Schreibe hierfür einfach !bet hh:mm:ss money. Als Beispiel: !bet 0:01:23 10. Wenn du vorher noch nicht gewettet hast, startest du mit 100 Münzen!",
                "help_start" : "Startet ein neues Rennen und gibt dir die Möglichkeit zu wetten!",
                "help_stop" : "Beendet einen Rennen und gibt jedem der gewettet hat einen gewissen Teil seines Einsatzes zurück. Die Menge ist abhängig von der Abweichung zur erreichten Zeit.",
                "help_reset" : "Setzt ein Rennen zurück und jeder erhält sein Geld wieder.",
                "help_help" : "Dies ist die Hilfe. Hier findest du alle Informationen die du über die Kommandos benötigt. Als Beispiel: !help help",
                "help_coins" : "Zeigt die Menge an Geld welche man besitzt.",
                "help_url" : "Erlaubt einem Nutzer eine URL zu schreiben. Als Beispiel: !url username",
                "help_priv" : "Um eine Aktion mit dem Bot auszuführen, benötigst du ein bestimmtes Befugnislevel. Mit dem Kommando !priv level username, kannst du das Befugnislevel setzen. Als Beispiel: !priv 42 serdrad0x",
                "help_remove" : "Du kannst ein selbst erstelltes Kommando entfernen mit !remove command. Als Beispiel: !remove !test",
                "help_setting" : "Du kannst di Einstellungen der automatischen Moderation ändern mit !setting warning_url/warning_caps on/off.",
                "help_follow" : "Wenn du möchtest, kann der Bot dir in den Channel folgen und bei der Moderation helfen. Für weitere Informationen schau doch einfach mal auf dem Bot_Omb Channel vorbei.",
                "help_unfollow" : "Wenn du Bot_Omb in deinem Chat verwendest und dort nicht mehr möchtest, dann kannst du ihn einfach entfernen mit !unfollow. Für weitere Informationen schau doch einfach mal auf dem Bot_Omb channel.",
                "help_greetings" : "Alle x Sekunden prüft der Bot auf neue Zuschauer und prüft ob diese bereits gegrüßt wurden. Um dieses Verhalten zu ändern nutze !setting greetings on/of und !setting greetings_interval 60",
                "help_poll" : "Wenn du schreibst !poll pollname (optionA / optionB) mm:ss dann kannst du eine zeitlich begrenzte Umfrage starten. !result zeigt dir die Ergebnisse und !vote num für das Abstimmen!",
                "help_next" : "Kündigt das nächste Level der Super Mario Maker - Level - Liste an.",
                "help_levels" : "Zeigt alle Level die zur Super Mario Maker - Level - Liste hinzugefügt wurden.",
                "help_submit" : "Fügt ein Level der Super Mario Maker - Level - Liste hinzu. Ein fremdes Level kann hinzugefügt werden über !submit username levelcode."
            }