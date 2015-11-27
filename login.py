import urllib
import urllib2
import json
import thread
import threading
import requests
import hashlib

reg_url = u"http://tubu.ibuzhai.com/rest/v1/sso/login"

def md5(str):
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()

def login(email, passwd):
	_data = {
		'app_version':"2.4.4",
		"device_type":1,
		"email":email,
		"password":md5(passwd)
	}
	s = requests.session()
	ret =s.post(reg_url, data = _data)
	print ret.status_code
	print ret.text

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global get_item_pics
		get_item_pics(self.item)	

if __name__ == "__main__":

	email = u"fuckme@fuck.com"
	name = u"fuckme"
	passwd = u"fuckme"
	login(email, passwd)
