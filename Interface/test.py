#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- initial author: 武笑石 -*-
# -*- other maintainers: 赵乙宁，汪元标 -*-
# -*- original name: testv3.py -*-

import requests, json
import time as systime
from datetime import datetime, timedelta
server_url_port = "127.0.0.1:8000"
session_id = None
record_id = []

def getCurTime():
	curtime = datetime.utcnow()
	curtime = curtime.strftime("%Y-%m-%d %H:%M:%S.%f")
	curtime = systime.strptime(curtime, "%Y-%m-%d %H:%M:%S.%f")
	curtime = systime.mktime(curtime)
	curtime = int(curtime * 1000)
	#curtime = str(curtime)
	return curtime

def isSuccess(response):
	success = True
	if not response.status_code == 200:
		success = False
	if "error" in response.text:
		success = False
	return success

def printResponse(response):
	print("    Status: " + str(response.status_code))
	print("    Text: " + response.text)
	print("    Headers: " + str(response.headers))

def checkInput(ins):
	if ins in ["logon", "login", "logout", "add", "delete", "update", "get", "query", "record_id", "quit" ]:
		return ins
	else:
		print ('''
Supported instructions:
	logon
	login
	logout
	add
	delete
	update
	get
	query
	record_id
	quit
''')
		return None

def logon():
	username = input("username:")
	password = input("password:")
	r = requests.post("http://" + server_url_port + r"/logon", \
		{
			"username": username,
			"password": password,
		})
	printResponse(r)

def login():
	global session_id
	username = input("username:")
	password = input("password:")
	r = requests.post("http://" + server_url_port + r"/login", \
		{
			"username": username,
			"password": password,
		}, cookies = {} if not session_id else {"session_id": session_id})
	if isSuccess(r):
		session_id = r.cookies.get("session_id")
		print('session id is ' + session_id)
	printResponse(r)

def logout():
	global session_id
	print('session id is ' + session_id)
	r = requests.post("http://" + server_url_port + r"/logout", \
		{}, cookies = {"session_id": session_id})
	if isSuccess(r):
		session_id = None
	printResponse(r)

def add():
	global record_id
	global session_id
	# for test, some field may not be given
	name = input("name: (push enter to skip)")
	time = input("time: (push enter to use current time)")
	if len(time) == 0:
		time = getCurTime()
	content = input("content: (push enter to skip)")
	record = {}
	if name:
		record["name"] = name
	if time:
		record["time"] = time
	if content:
		record["content"] = content
	print(record)
	r = requests.post("http://" + server_url_port + r"/record/add", \
		record, cookies = {"session_id": session_id})
	printResponse(r)
	if isSuccess(r):
		record_id.append(json.loads(r.text)["record_id"])

def delete():
	global session_id
	record = -1
	record = input("Which to delete?")
	r = requests.post("http://" + server_url_port + r"/record/" + str(record) + "/delete", \
		{}, cookies = {"session_id": session_id})	
	try:
		record = int(record)
	except:
		print("record is not a number. should not delete anything")
	else:
		if isSuccess(r):
			record_id.remove(str(record))
	printResponse(r)

def update():
	global session_id
	record = -1
	_id = input("Which to update?")
	name = input("name: (push enter to skip)")
	time = input("time: (push enter to use current time)")
	if len(time) == 0:
		time = getCurTime()
	content = input("content: (push enter to skip)")
	record = {}
	if name:
		record["name"] = name
	if time:
		record["time"] = time
	if content:
		record["content"] = content
	r = requests.post("http://" + server_url_port + r"/record/" + str(_id) + "/update", \
		record, cookies = {"session_id": session_id})
	try:
		_id = int(_id)
	except:
		print("id is not a number. should not delete anything")
	printResponse(r)

def get():
	global session_id
	record = -1
	record = input("Which to get?")
	try:
		record = int(record)
	except:
		print("not a number.")
	if not type(record) == type(1):
		return
	r = requests.get("http://" + server_url_port + r"/record/" + str(record), cookies = {"session_id": session_id})
	printResponse(r)

def query():
	global session_id
	name = input("filter name?")
	if not name:
		name = ""
	r = requests.get("http://" + server_url_port + r"/record/query?name=" + name, \
		{}, cookies = {"session_id": session_id})
	printResponse(r)

def show_record_id():
	print("current record_id: " + str(record_id))
	return




while True:
	ins = None
	while not ins:
		ins = input()
		ins = checkInput(ins)

	if ins == "logon":
		logon()
	elif ins == "login":
		login()
	elif ins == "logout":
		logout()
	elif ins == "add":
		add()
	elif ins == "delete":
		delete()
	elif ins == "update":
		update()
	elif ins == "get":
		get()
	elif ins == "query":
		query()
	elif ins == "record_id":
		show_record_id()
	else:
		quit()

