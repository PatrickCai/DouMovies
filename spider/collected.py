#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

import requests
from bs4 import BeautifulSoup

from role.celebrity  import Celebrity
from spider import get_soup


reload(sys)
sys.setdefaultencoding('utf-8')

celebrities_IDs = []
celebrities = []
def get_celebrities(username, start_number):
	url = 'http://movie.douban.com/people/%s/celebrities?start=%s'%(username, start_number)
	soup = get_soup(url)
	page_celebrities = soup.findAll('a',  href=re.compile('http://movie.douban.com/celebrity/\d{7}/$'))
	page_celebrities = set([re.search('\d{7}', celebrity['href']).group() for celebrity in page_celebrities])
	page_celebrities = [Celebrity(page_celebrity, collect_or_watch='collect') for page_celebrity in page_celebrities]
	celebrities.extend(page_celebrities)


def get_celebrities_pages(username):
	url = 'http://movie.douban.com/people/%s/celebrities'%(username)
	soup = get_soup(url)
	title = soup.title.text
	pages = int(re.search('\((\d+)\)$', title).group(1))	
	return pages





