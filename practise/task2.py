import sys
import base64
import re
import hashlib
from math import *

def input_all():
    global username
    global password_encoded
    global password
    username = sys.stdin.readline()
    if username[-1] == '\n':
        username = username[0 : -1]
    '''password = sys.stdin.readline()
    if password[-1] == '\n':
        password = password[0:-1]'''
    password_encoded = sys.stdin.readline()
    if password_encoded[-1] == '\n':
        password_encoded = password_encoded[0:-1]
    password = str(base64.b64decode(password_encoded))[2:-1]
    print(username,password)

def judge_username():
    pattern_1 = re.compile(r'[^a-zA-Z0-9 ~@&*-_+.,]')
    pattern_2_1 = re.compile(r'^ ')
    pattern_2_2 = re.compile(r' $')
    pattern_3 = re.compile(r'@')
    pattern_4 = re.compile(r'[a-zA-Z]')
    list_1 = re.findall(pattern_1, username)
    list_2_1 = re.findall(pattern_2_1, username)
    list_2_2 = re.findall(pattern_2_2, username)
    list_3 = re.findall(pattern_3, username)
    list_4 = re.findall(pattern_4, username)
    if len(list_1) != 0:
        return False
    if len(list_2_1) != 0:
        return False
    if len(list_2_2) != 0:
        return False
    if len(list_3) > 1:
        return False
    if len(list_4) < 3:
        return False
    if len(username) < 4 or len(username) > 32:
        return False
    return True

def judge_password():
    pattern_1_1 = re.compile(r'^[ \t\r\n]')
    pattern_1_2 = re.compile(r'[ \t\r\n]$')
    pattern_2_1 = re.compile(r'[a-zA-Z]')
    pattern_2_2 = re.compile(r'[0-9]')
    list_1_1 = re.findall(pattern_1_1, password)
    list_1_2 = re.findall(pattern_1_2, password)
    list_2_1 = re.findall(pattern_2_1, password)
    list_2_2 = re.findall(pattern_2_2, password)
    if len(list_1_1) != 0:
        return False
    if len(list_1_2) != 0:
        return False
    if len(list_2_1) == 0:
        return False
    if len(list_2_2) == 0:
        return False
    if password.find(username) != -1:
        return False
    if len(password) < 6 or len(password) > 20:
        return False
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] and password[i] == password[i + 2]:
            return False
    return True
    




def main():
    global all_string
    input_all()
    if judge_username() == False:
        sys.stderr.write('invalid')
        return
    if judge_password() == False:
        sys.stderr.write('invalid')
        return
    all_string = username + '|' + password
    #print(all_string)
    md5_val = hashlib.md5(all_string.encode('utf8')).hexdigest()
    sys.stdout.write(str(md5_val))

if __name__ == '__main__':
    main()
