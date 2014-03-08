#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

import requests
import cPickle
from bs4 import BeautifulSoup
from random import choice
import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')

proxies_pickle = cPickle.load(open('daili', 'r'))
proxies = [{'http':'http://%s'%(proxy)} for proxy in proxies_pickle ]
proxy = choice(proxies)

def get_soup(url, proxy=proxy, timeout=50):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
			   'Accept-Encoding': 'gzip, deflate',
				'DNT': '1',
				'Connection': 'keep-alive'}

	try:
		proxy = choice(proxies)
		req = requests.get(url,proxies=proxy, timeout=timeout, headers=headers)
		if req.status_code == 200:
			soup = BeautifulSoup(req.content)
		else :
			proxy = choice(proxies)
			print('change the proxy')
			soup = get_soup(url, proxy=proxy)

	except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
		print(e)
		print('Change the proxy')
		proxy = choice(proxies)
		soup = get_soup(url, proxy=proxy)


	return soup
