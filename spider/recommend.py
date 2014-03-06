#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os

import gevent.monkey
gevent.monkey.patch_socket()

dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

from spider import get_soup

reload(sys)
sys.setdefaultencoding('utf-8')

def get_movies(username, ID, start_number):
	url = 'http://movie.douban.com/celebrity/%s/movies?start=%s&format=text&sortby=vote&'%(ID, start_number)
	soup = get_soup(url)