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

def save(file_path, data):
    file_save = open(file_path, 'w')
    for i in range(len(data)):
        output = ''
        for j in range(len(data[i])):
            output += str(data[i][j]) + ";"
        file_save.write(output[:len(output)-1]+"\n")
    file_save.close()
    
def load(file_path):
    with open(file_path, 'r') as loaded:
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

def update(key, data, frm):
    for i in range(len(frm)):
        if key in frm[i]:
            for j in range(len(frm[i])):
                if data[j] != None:
                    frm[i][j] = data[j]
            return True
    return False
    
def get_element(key, frm):
    for elem in frm:
        if key in elem:
            return elem
    return None

def create(files):
    for key in files:
        key_file = open(key["file_path"]+key["file_name"], "w")
        key_file.write(key["file_data"])
        key_file.close()

def show(elements):
    for i in range(len(elements)):
        print(elements[i])

def has(arr, element):
    for key in arr:
        if key[0] == element:
            return True
    return False

def string_to_bool(message):
    if message == "True":
        return True
    return False

def isNumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False