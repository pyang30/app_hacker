#!/usr/bin/env python

import urllib
import urllib2
import json
import thread
import threading
import requests
import os

fav_url = u"http://tubu.ibuzhai.com/rest/v3/favorite"

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global download_pic
		download_pic(self.item)	

def do_fav(_id, token, s, fav=True):
	_obj = [{
		"object_id":	_id,
		"cancel":	not fav,
		"object_type":	2,
		"logs_id":	0	
	}]
	_data = {
		"access_token":token,
		"app_version":"2.4.4",
		"device_type":1,
		"object" : json.dumps(_obj)
	}
	r = requests.post(fav_url, data = _data)
	return True if r.status_code == 200 else False
