#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os

dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

reload(sys)
sys.setdefaultencoding('utf-8')

class Comment(object):
	def __init__(self, content, author, star):
		self.name = content
		self.author = author
		self.star = star