import urllib
import urllib2
import json
import thread
import threading

url = u"http://tubu.ibuzhai.com/rest/v1/travelog/recommends?app_version=2.4.4&device_type=1&page=1&page_size=2000"
item_url = u"http://tubu.ibuzhai.com/rest/v2/travelog/"
travels = []

def get_item_pics(item):
	sub_url = item_url + item['id']
	print sub_url
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

if __name__ == "__main__":
	results = []	

	res = urllib2.urlopen(url)
	data = res.read()
    #print data
	data = json.loads(data) 
	print data.keys()
	print data['total']
	print data['total_pages']
	print data['cur_page']
	data_list = data['logs']

	for item in data_list:
		content = {}
		temp = []
		content["id"] = item["id"]
		content["pics"] = temp
		results.append(content)	

	print len(results)
	thread_pool = []	
	counter = 0
	for item in results:
		thread = Process(item)
		thread_pool.append(thread)
		counter += 1
		thread.start()
		if counter % 10 == 0:
			for t in thread_pool:
				t.join()
			thread_pool = []	
		for t in thread_pool:
			t.join()
		thread_pool = []	
	print len(results)
	
	with open("url.txt", 'w') as f:
		for item in results:
			for pic in item['pics']:
				f.write(pic + "\n")		
	
