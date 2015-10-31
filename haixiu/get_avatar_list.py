#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import json
import thread
import threading
import requests
import hashlib
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
update_user_url = u"http://tubu.ibuzhai.com/rest/v2/user/update"
reg_url = u"http://tubu.ibuzhai.com/rest/v1/sso/login"

def md5(str):
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()

def get_item_pics(item):
	sub_url = item_url + item['id']
	global travels
	travels.append(sub_url)

	pics = item['pics']
	res = urllib2.urlopen(sub_url)
	data = json.loads(res.read())
	pics_list = data['log']['posts']
	for pic in pics_list:
		pics.append(pic['pictures'][0]['picture'])
	

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global get_item_pics
		get_item_pics(self.item)	

def login(email, passwd, s):
	_data = {
		'app_version':"2.4.4",
		"device_type":"1",
		"email":email,
		"password":md5(passwd)
	}
	ret =s.post(reg_url, data = _data)
	if ret.status_code == 200:
		return json.loads(ret.text)
	else:
		print "%s login failed" % email
		return None

def update_user(token, s, avatar, jsr, names):
	_data = {
		'access_token': token,
		'app_version': "2.4.4",
		'avatar': avatar,
		'city_id': jsr['city_id'],
		'device_type': 1,
		'district_id': jsr['district_id'],
		'gender': "m" if random.randint(1,1000)%2 == 0 else "f",
		'location': u'上海',
		'nickname': random.choice(names),
		'province_id': 3
			}
	r = s.post(update_user_url, data = _data)	
	return True if r.status_code == 200 else False

if __name__ == "__main__":
	results = []	
	avatars = []
	names = []
	r = requests.get(url)
	l = json.loads(r.text)['logs']

	for a in l:
		avatar = a['created_by']['avatar']
		avatars.append(avatar)
	with open('b.txt', 'r') as f:
		names = f.readlines()

	with open('account.txt', 'r') as f:
		for line in f.readlines():
			d = line.split('\t')
			email = d[0]
			name = d[1]
			passwd = d[2].strip()
			s = requests.session()
			jsr = login(email, passwd, s)
			a = random.choice(avatars)
			ret = update_user(jsr['access_token'], s, a, jsr, names)
			if ret:
				print ("update %s done" % name) 
			else:
				print "failed"
