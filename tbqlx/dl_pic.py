#!/usr/bin/env python
import urllib
import urllib2
import json
import thread
import threading
import os
import requests

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
travels = []
pwd = os.path.abspath('.')

def download_pic(item):
	res = urllib2.urlopen(item)
	data = res.read()
	name = os.path.basename(item)	
        name += ".jpg"
	fullpath = os.path.join(pwd, 'pics')
	fullpath = os.path.join(fullpath, name)
	fullpath = fullpath.strip()
	print fullpath
	with open(fullpath, 'w') as f:
		f.write(data)


class Process(threading.Thread):
	def __init__(self, item):
		threading.Thread.__init__(self)
		self.item = item

	def run(self):
		global download_pic
		download_pic(self.item)	

def download_all_pics():
    with open('tubu_pic.txt', 'r') as f:
	results = f.readlines()
   	print len(results)
   	thread_pool = []	
   	counter = 0
   	for item in results:
            thread = Process(item)
   	    thread_pool.append(thread)
   	    counter += 1
   	    thread.start()
   	    if counter % 40 == 0:
   		for t in thread_pool:
   	            t.join()
   		    thread_pool = []	
   		    counter = 0
def download_pics_by_id(_id):
    url = item_url + str(_id)
    ret = requests.get(url)
    data = ret.text
    posts = json.loads(data)['log']['posts']
    pics = []
    for p in posts:
        pic = p['pictures'][0]['picture']
        pics.append(pic)
        download_pic(pic)
if __name__ == "__main__":
    download_pics_by_id(4021)
