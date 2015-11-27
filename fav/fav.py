import urllib
import urllib2
import json
import thread
import threading
import requests
import os

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"

login_url = u"http://tubu.ibuzhai.com/rest/v1/sso/login"
email = u"fgmuhwcb@www.bccto.me"
pwd_md5 = u"d01cd3370612e35f1ab962d6cd90b944"
fav_url = u"http://tubu.ibuzhai.com/rest/v3/favorite"

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global download_pic
		download_pic(self.item)	
def do_fav(_id, token, s):
	_obj = [{
		"object_id":_id,
		"cancel":"false",
		"object_type":2,
		"logs_id":0	
	}]
	_data = {
		"access_token":token,
		"app_version":"2.4.4",
		"device_type":2,
		"object" : _obj
	}
	r = requests.post(fav_url, data = _data)
	print len(r.raw.data)

if __name__ == "__main__":
	_data = {
	"app_verion":"2.4.4",
	"device_type":2,
	"email": email,
	"password": pwd_md5
	}	
	s = requests.session()
	r = s.post(login_url, data = _data)
	print r.text
	token = json.loads(r.text)['access_token']
	print token	
	token = u"a429d124-6151-46d4-ad7d-cf3c986042b0"
	do_fav(4736, token, s)
