#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys

import requests
from bs4 import BeautifulSoup
import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')


proxies={
	'http':'http://211.138.121.37:82'
}
def get_soup(url):
	req = requests.get(url,proxies=proxies)
	if req.status_code == 200:
		soup = BeautifulSoup(req.content)
	else :
		print(req.status_code)
		print('Cannot connect')
		exit(0)		

	return soup
