from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import sqlite3
import json
import random
import time
import datetime
import pytz
from math import *

#判断是否已经登录，如果登录就返回user_name,否则返回none
def judge_whether_loaded(request):
    try:
        session_id = request.COOKIES['session_id']
    except:
        return None
        #连接数据库
    #print(session_id)
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    #查询用户名
    cursor.execute('select * from login_user where session=?', (session_id,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    if len(values) == 0:
        return None
    else:
        if values[0][2] == 1:
            return values[0][0]
        else:
            return None

#判断是否已经登录，如果登录就返回True,否则false，纯用于login.思路：user和session都能找到，且状态true才行
def judge_whether_loaded_user(request):
    username = request.POST["username"]
    try:
        session_id = request.COOKIES['session_id']
    except:
        return False
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    #查询用户名
    cursor.execute('select * from login_user where username=?', (username,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    #print(values, session_id)
    if len(values) == 0:
        return False
    else:
        for item in values:
            if int(item[1]) == int(session_id) and item[2] == 1:
                return True
    return False

def generate_random_session():
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    while True:
        random_session = floor(random.random()*114514)
        cursor.execute('select * from login_user where session=?', (random_session,))
        values = cursor.fetchall()
        if len(values) == 0:
            #关闭Cursor:
            cursor.close()
            #提交事务:
            conn.commit()
            #关闭Connection:
            conn.close()
            return random_session

def generate_new_id():
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    new_id = 0
    cursor = conn.cursor()
    cursor.execute('select * from history_record')
    values = cursor.fetchall()
    for item in values:
        if item[3] > new_id:
            new_id = item[3]
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    return (new_id + 1)

#获取url的id
def get_id(request):
    #print(request.path)
    url = request.path
    the_list = url.split('/')
    number = -1
    try:
        number = int(the_list[-1])
    except:
        number = int(the_list[-2])
    return number

#将时间戳转换成北京时间
def switch_time(time_stamp):
    mili_second = time_stamp % 1000
    new_time_stamp = floor(time_stamp / 1000)
    time_array = time.localtime(new_time_stamp) 
    time_real = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    time_real += '.'
    time_real += str(mili_second) 
    print(time_real)
    return time_real

def logon(request):
    #定义返回格式
    return_invalid = {"error": "invalid parameters"}
    return_has_user = {"error": "user exists"}
    return_right = {"user": 0}
    return_data = {}
    #读取用户名，密码，并且判断是否为空
    username = None
    password = None
    try:
        username = request.POST["username"]
    except:
        return HttpResponse(json.dumps(return_invalid, ensure_ascii = False), content_type="application/json")
    try:
        password = request.POST["password"]
    except:
        return HttpResponse(json.dumps(return_invalid, ensure_ascii = False), content_type="application/json")
    if username == None or password == None or len(username) == 0 or len(password) == 0:
        return HttpResponse(json.dumps(return_invalid, ensure_ascii = False), content_type="application/json")  
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    #查询用户名
    cursor.execute('select * from user_info where username=?', (username,))
    values = cursor.fetchall()
    if len(values) == 0:
        #添加数据
        secret_password = make_password(password)
        sql_insert = 'insert into user_info (username, password) values (:username, :password)'
        cursor.execute(sql_insert,{"username":username,"password":secret_password})
        return_right["user"] = username
        return_data = return_right
    else:
        return_data = return_has_user
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    return HttpResponse(json.dumps(return_data, ensure_ascii = False), content_type="application/json")

    

def login(request):
    #定义返回信息
    return_nouser = {'error': "no such a user"} 
    return_wrong_pass = {'error': "password is wrong"}
    return_has_log_in = {'error': 'has logged in'}
    return_normal = {'user': 0}
    #读取用户名，密码，并且判断是否为空
    username = None
    password = None
    try:
        username = request.POST["username"]
    except:
        return HttpResponse(json.dumps(return_nouser, ensure_ascii = False), content_type="application/json")
    try:
        password = request.POST["password"]
    except:
        return HttpResponse(json.dumps(return_wrong_pass, ensure_ascii = False), content_type="application/json")   
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    #查询用户名
    cursor.execute('select * from user_info where username=?', (username,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()

    #测试
    #print(values[0][1])
    #print(password)

    if len(values) == 0:
        #用户名不存在
        return HttpResponse(json.dumps(return_nouser, ensure_ascii = False), content_type="application/json")

    else:
        if check_password(password, str(values[0][1]))!= True:
            #密码错误
            return HttpResponse(json.dumps(return_wrong_pass, ensure_ascii = False), content_type="application/json")
        else:
            whether_has_logged = judge_whether_loaded(request)
            if whether_has_logged == None:
                #没登录过，正确
                return_normal['user'] = username
                response = HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")

                #生成随机session并且存储
                new_session = generate_random_session()
                sql_insert = 'insert into login_user (username, session, whether) values (:username, :session, :whether)'    #连接数据库
                conn = sqlite3.connect('main.db')
                #创建一个Cursor:
                cursor = conn.cursor()
                cursor.execute(sql_insert,{"username":username,"session":new_session,"whether":1})
                #关闭Cursor:
                cursor.close()
                #提交事务:
                conn.commit()
                #关闭Connection:
                conn.close()

                response.set_cookie(key = 'session_id', value = new_session)
                return response
            else:
                #已经登录
                return HttpResponse(json.dumps(return_has_log_in, ensure_ascii = False), content_type="application/json")


def logout(request):
    #定义返回信息
    return_not_post = {'error': "require POST"}
    return_no_session = {'error': 'no valid session'}
    return_normal = {'user':0}
    #判断是否是get
    if request.method != 'POST':
        return HttpResponse(json.dumps(return_not_post, ensure_ascii = False), content_type="application/json") 
    #判断session是否有效
    user_name = judge_whether_loaded(request)
    if(user_name == None):
        #未登录
        return HttpResponse(json.dumps(return_no_session, ensure_ascii = False), content_type="application/json")
    else:
        #已经登录：注销session
        session_id = request.COOKIES['session_id']
        #连接数据库
        conn = sqlite3.connect('main.db')
        #创建一个Cursor:
        cursor = conn.cursor()
        sql_change = "update login_user set whether = :whether where username = :username AND session = :session"
        cursor.execute(sql_change, {"whether": 0, "username": user_name, "session":session_id})
        #关闭Cursor:
        cursor.close()
        #提交事务:
        conn.commit()
        #关闭Connection:
        conn.close()  
        return_normal['user'] = user_name
        return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")


    


def add_record(request):
    #定义错误信息
    return_not_login = {'error': 'please login'}
    return_invalid_parameter = {'error': "invalid parameters"}
    return_normal = {'record_id': 0}
    #获取参数，判合理判空
    name = None
    time = None
    content = None
    try:
        name = request.POST["name"]
        if len(name) == 0:
            return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    except:
        return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    try:
        content = request.POST["content"]
        if len(content) == 0:
            return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    except:
        return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    try:
        time = int(request.POST["time"])
        if time <= 0:
            return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    except:
        return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    #判断是否登录
    user_name = judge_whether_loaded(request)
    if user_name == None:
        #未登录
        return HttpResponse(json.dumps(return_not_login, ensure_ascii = False), content_type="application/json")
    #生成新id，返回
    new_id = generate_new_id()
    return_normal['record_id'] = new_id
    #存储
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    sql_insert = 'insert into history_record (name, time, content, id, username) values (:name, :time, :content, :id, :username)'
    cursor.execute(sql_insert,{"name":name,"time":time, "content":content, "id":new_id, "username":user_name})
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")
    




def delete_record(request):
    #定义错误信息
    return_not_login = {'error': 'please login'}
    return_not_post = {'error': "require POST"}
    return_invalid_parameter = {'error': "invalid parameters"}
    return_unknown_record = {'error': 'unknown record'}
    return_normal = {'record_id': 0}
    #判断是否是get
    if request.method != 'POST':
        return HttpResponse(json.dumps(return_not_post, ensure_ascii = False), content_type="application/json") 
    #判断是否登录
    user_name = judge_whether_loaded(request)
    if user_name == None:
        #未登录
        return HttpResponse(json.dumps(return_not_login, ensure_ascii = False), content_type="application/json")
    #获取id
    the_id = get_id(request)
    #查询记录
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    cursor.execute('select * from history_record where id=?', (the_id,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()

    if the_id <= 0:
        #不合法
        return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    if len(values) == 0:
        #没有记录
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    if values[0][4] != user_name:
        #不是自己的数据
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    #合法
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    cursor.execute("delete from history_record where id =?", (the_id,))
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()  
    return_normal['record_id'] = the_id
    return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")

def update_record(request):
    #定义错误信息
    return_not_login = {'error': 'please login'}
    return_not_post = {'error': "require POST"}
    return_invalid_parameter = {'error': "invalid parameters"}
    return_unknown_record = {'error': 'unknown record'}
    return_unknown_record_field = {'error': 'unknown record field'}
    return_normal = {'record_id': 0}
    #判断是否是get
    if request.method != 'POST':
        return HttpResponse(json.dumps(return_not_post, ensure_ascii = False), content_type="application/json") 
    #获取参数，判合理判空
    name = None
    time = None
    content = None
    try:
        name = request.POST["name"]
    except:
        name = None
    try:
        content = request.POST["content"]
    except:
        content = None
    try:
        time_input = request.POST["time"]
        try:
            time = int(time_input)
            if time <= 0:
                #不是正整数
                return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
        except:
            #不是整数
            return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    except:
        #参数不存在
        time = None
    #判断是否有别的参数
    for key in request.POST.keys():
        if key != 'name' and key != 'content' and key != 'time':
            return HttpResponse(json.dumps(return_unknown_record_field, ensure_ascii = False), content_type="application/json")
    #判断是否登录
    user_name = judge_whether_loaded(request)
    if user_name == None:
        #未登录
        return HttpResponse(json.dumps(return_not_login, ensure_ascii = False), content_type="application/json")
    #获取id
    the_id = get_id(request)
    #查询记录
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    cursor.execute('select * from history_record where id=?', (the_id,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()

    if the_id <= 0:
        #不合法
        return HttpResponse(json.dumps(return_invalid_parameter, ensure_ascii = False), content_type="application/json")
    if len(values) == 0:
        #没有记录
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    if values[0][4] != user_name:
        #不是自己的数据
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    #合法
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    if name != None:
        sql_name = "update history_record set name = :name where id = :id"
        cursor.execute(sql_name, {"name": name, "id": the_id})
    if time != None:
        sql_time = "update history_record set time = :time where id = :id"
        cursor.execute(sql_time, {"time": time, "id": the_id})
    if content != None:
        sql_content = "update history_record set content = :content where id = :id"
        cursor.execute(sql_content, {"content": content, "id": the_id})
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()  
    return_normal['record_id'] = the_id
    return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")

def get_record(request):
    #定义错误信息
    return_not_login = {'error': 'please login'}
    return_unknown_record = {'error': 'unknown record'}
    return_normal = {'record_id': 0, "name": 0, "content": 0, "time": 0} 
    #判断是否登录
    user_name = judge_whether_loaded(request)
    if user_name == None:
        #未登录
        return HttpResponse(json.dumps(return_not_login, ensure_ascii = False), content_type="application/json")
    #获取id
    the_id = get_id(request)
    #查询记录
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    cursor.execute('select * from history_record where id=?', (the_id,))
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()

    if len(values) == 0:
        #没有记录
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    if values[0][4] != user_name:
        #不是自己的数据
        return HttpResponse(json.dumps(return_unknown_record, ensure_ascii = False), content_type="application/json")
    #合法
    return_normal['record_id'] = the_id
    return_normal['name'] = values[0][0]
    return_normal['content'] = values[0][2]
    return_normal['time'] = switch_time(int(values[0][1]))
    return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")

def query_record(request):
    #定义错误信息
    return_not_login = {'error': 'please login'}
    return_no_name = {'error': 'need name words'}
    return_normal = {'list': None} 
    #判断是否登录
    user_name = judge_whether_loaded(request)
    if user_name == None:
        #未登录
        return HttpResponse(json.dumps(return_not_login, ensure_ascii = False), content_type="application/json")
    #获取参数
    name = None
    try:
        name = request.GET["name"]
        if len(name) == 0:
            return HttpResponse(json.dumps(return_no_name, ensure_ascii = False), content_type="application/json")
    except:
        return HttpResponse(json.dumps(return_no_name, ensure_ascii = False), content_type="application/json")
    #查询记录
    #连接数据库
    conn = sqlite3.connect('main.db')
    #创建一个Cursor:
    cursor = conn.cursor()
    #查询所有本username的数据
    #"select * from cat where  name like '%"+d+"%'"
    sql = "select * from history_record where name like '%"+str(name)+"%'"
    #print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    #关闭Cursor:
    cursor.close()
    #提交事务:
    conn.commit()
    #关闭Connection:
    conn.close()
    #提取信息
    return_list = []
    for item in values:
        if item[4] == user_name:
            return_dict = {}
            return_dict["record_id"] = item[3]
            return_dict["name"] = item[0]
            return_dict["content"] = item[2]
            return_dict["time"] = switch_time(int(item[1]))
            return_list.append(return_dict)
    return_normal['list'] = return_list
    return HttpResponse(json.dumps(return_normal, ensure_ascii = False), content_type="application/json")
