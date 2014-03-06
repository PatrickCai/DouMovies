#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys


reload(sys)
sys.setdefaultencoding('utf-8')

class Movie(object):
	def __init__(self, ID, name):
		self.ID = ID
		self.name = name
