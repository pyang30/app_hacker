#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import json
import thread
import threading
import requests
import random
import hashlib
from fav import do_fav
from comment import do_comment
from comment_pic import do_comment_pic
from register import get_name

reg_url = u"http://tubu.ibuzhai.com/rest/v1/sso/login"
#travel_log = u"http://tubu.ibuzhai.com/rest/v2/travelog/4736?access_token=cadef06b-d17e-47d0-8533-d0df838f0f03&app_version=2.4.4&device_type=1"
travel_log = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
#recommend_url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=20"
recommend_url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends"

def get_recommend_count(count):
	_params = {
		"app_version": "2.4.4",
		"device_type": 1,
		"page_size": count
		}
	r = requests.get(recommend_url, params = _params)
	return r.text

def get_travel_log_by_id(_id, token):
	_params = {
		"access": token,
		"app_version": "2.4.4",
		"device_type": 1
		}
	url = travel_log + str(_id)
	r = requests.get(url, params = _params)
	return  r.text

def get_trail_id_by_travel_id(_id):
	data = get_recommend_count(1000)
	lst_data = json.loads(data)['logs']
	target = filter(lambda x: x['id'] == str(_id), lst_data)
	return int(target[0]['trail_id'])

def md5(str):
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()

def login(email, passwd, s):
	_data = {
		'app_version':"2.4.4",
		"device_type":"1",
		"email":email,
		"password":md5(passwd)
	}
	ret =s.post(reg_url, data = _data)
	if ret.status_code == 200:
		return json.loads(ret.text)['access_token']
	else:
		print "%s login failed" % email
		return None

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global get_item_pics
		get_item_pics(self.item)	

comment_list = None
def get_one_comment():
	global comment_list
	if comment_list == None:
		with open('comment.txt', 'r') as f:
			comment_list = f.readlines()
	
	return random.choice(comment_list)

def comment_all_pics_by_travel_id(_id):
	email = u"fuckme@fuck.com"
	name = u"fuckme"
	passwd = u"fuckme"

	s = requests.session()
	token = login(email, passwd, s)

	log_data = get_travel_log_by_id(_id, token)

	post_list = json.loads(log_data)['log']['posts']
	pic_list = [int(pic['id']) for pic in post_list]
	
	for _id in pic_list:
		comment = get_one_comment()
		print comment
		ret = do_comment_pic(_id, token, s, comment )
		if ret:
			print("comment successfully")

def thumbs_up(_id, count):
	email = u"fuckme@fuck.com"
	name = u"fuckme"
	passwd = u"fuckme"

	s = requests.session()
	token = login(email, passwd, s)
	for i in range(count):
		do_fav(_id, token, s, True)

if __name__ == "__main__":
	#comment_all_pics_by_travel_id(4784)
	thumbs_up(4803, 500)
	'''
	s = requests.session()
	s.headers = {
		'Accept' :			'*/*',
		'Accept-Encoding':	'gzip, deflate',
		'Accept-Language':	'zh-Hans-CN;q=1, en-CN;q=0.9',
		'User-Agent' :		'Tubuqu IOS 2.4.4 / iPhone 5s / 9.1 / WIFI',
	#	'Content-Length':	474,
		'Content-Type':		'application/x-www-form-urlencoded',
		'Connection' :		'Keep-Alive',
		'Connection' :		'Keep-Alive',
		'Host':				'tubu.ibuzhai.com'
	}

	email = u"fuckme@fuck.com"
	name = u"fuckme"
	passwd = u"fuckme"
	token = login(email, passwd, s)
	print token
	print 20 * ">>"
	get_recommend_count(1)	
	for i in range(1000):
		r = do_fav(4736, token, s, True)
	get_recommend_count(1)	
	trail_id = get_trail_id_by_travel_id(4736)

	with open('account.txt', 'r') as f:
		for line in f.readlines():
			d = line.split('\t')
			email = d[0]
			name = d[1]
			passwd = d[2].strip()
			s = requests.session()
			token = login(email, passwd, s)
			comment = requests.get("http://whatthecommit.com/index.txt").text
			do_comment(trail_id, 4736, token, s, comment)
			print "%s post a comment:%s " % (name, comment)
	print 20 * "<<"
	'''
