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
	'http':'http://58.215.52.152:8080'
}
def get_soup(url):
	req = requests.get(url, proxies=proxies)
	if req.status_code == 200:
		soup = BeautifulSoup(req.content)
	else :
		print('Cannot connect')
		exit(0)		

	return soup
