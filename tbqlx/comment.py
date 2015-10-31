#!/usr/bin/env python

import urllib
import urllib2
import json
import thread
import threading
import requests
import os

comment_url = u"http://tubu.ibuzhai.com/rest/v1/trail/%d/trailog/%d/comments"

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global download_pic
		download_pic(self.item)	

def do_comment(_trail_id, _id, token, s, comment, parent_id=0):
	_data = {
		"access_token":	token,
		"app_version":	"2.4.4",
		"comment":		comment,
		"device_type":	1,
		"parent_id":	parent_id,
		"traid_id":		_trail_id,
		"trailog_id":	_id
	}
	url = comment_url % (_trail_id, _id)
	r = s.post(url, data = _data)
	return True if r.status_code == 200 else False
