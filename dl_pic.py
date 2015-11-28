import urllib
import urllib2
import json
import thread
import threading
import os

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
travels = []
pwd = os.path.abspath('.')

def download_pic(item):
	res = urllib2.urlopen(item)
	data = res.read()
	name = os.path.basename(item)		
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

if __name__ == "__main__":
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
		if counter % 100 == 0:
			for t in thread_pool:
				t.join()
			thread_pool = []	
		for t in thread_pool:
			t.join()
		thread_pool = []	
	print len(results)
