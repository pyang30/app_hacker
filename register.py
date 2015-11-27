import urllib
import urllib2
import json
import thread
import threading
import requests
import hashlib
import random
import string

reg_url = u"http://tubu.ibuzhai.com/rest/v1/sso/register"

def md5(str):
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()

def get_name():
	length = random.randint(6, 12)
	name = ''.join(random.sample(string.lowercase, length))
	return name

def get_email_server():
	length = random.randint(4, 6)
	server = ''.join(random.sample(string.lowercase, length))
	return server

def get_passwd():
	length = random.randint(6, 8)
	passwd = ''.join(random.sample(string.lowercase+string.digits, length))
	return passwd

def get_email():
	name = get_name()
	server = get_email_server()
	email = ''.join([name, '@', server, '.com'])
	return email

def register_count(email, name, passwd):
	_data = {
		'app_version':"2.4.4",
		"device_type":1,
		"email":email,
		"nickname":name,
		"password":md5(passwd)
	}
	s = requests.session()
	ret =s.post(reg_url, data = _data)
	if int(ret.status_code) == 200:
		return True
	else:
		return False

class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global get_item_pics
		get_item_pics(self.item)	

if __name__ == "__main__":
	for i in range(2):
		email = get_email()
		name = get_name()
		pwd = get_passwd()
		account = "\t".join([email, name, pwd])
		ret = register_count(email, name, pwd)
		if ret:
			print("register %s successfully" % email)

			with open("account.txt", 'a+') as f:
				f.write(account + '\n')
		else:
			print("register %s failed" % email)

