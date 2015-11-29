#!/usr/bin/env python

import urllib
import urllib2
import json
import thread
import threading
import requests
import os

comment_url = u"http://tubu.ibuzhai.com/rest/v1/travelog/post/%s/comment"

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global download_pic
		download_pic(self.item)	

def do_comment_pic(_pic_id, token, s, comment):
	_data = {
		"access_token":	token,
		"app_version":	"2.4.4",
		"comment":		comment,
		"device_type":	1,
		"parent_id":	0,
	}
	url = comment_url % (_pic_id)
	r = s.post(url, data = _data)
	return True if r.status_code == 200 else False
