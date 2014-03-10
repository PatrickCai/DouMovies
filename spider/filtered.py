#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os
import re

import gevent.monkey
gevent.monkey.patch_socket()

dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

from doulist.doulist import Movie_list
from spider import get_soup

from role.movie import Recommend_movie
from role.comment import Comment

reload(sys)
sys.setdefaultencoding('utf-8')

final_movies = Movie_list()
def get_final_movies(movie):
	url = 'http://movie.douban.com/subject/%s/'%(movie.ID)
	soup = get_soup(url, timeout=15)
	is_movie = not bool(soup.find('div', class_='episode_list'))

	def find_author_comment(star):
		star = soup.find('span', class_=("allstar%s0 rating"%(star)))
		if star:
			comment = star.parent.parent.next_sibling.next_sibling.next
			author = star.previous_sibling.previous_sibling.text
		else:
			comment = None
			author = None
		return comment, author
	if is_movie:
		four_comment,four_author = find_author_comment(4) 
		five_comment,five_author = find_author_comment(5) 
		movie.comment = [Comment(four_comment, four_author, 4), 
						 Comment(five_comment, five_author, 5)]
	#Poster url
		poster_url = soup.find('img', {'rel':'v:image'}, {'title':u'点击看更多海报'})['src']
		movie.poster_url = poster_url
		print('5.Ok %s'%(movie.ID))
		final_movies.append(movie)

existing_movies = []
def get_special(celebrity):
	url = 'http://movie.douban.com/celebrity/%s/'%(celebrity.ID)
	soup = get_soup(url, timeout=12)
	image_url = soup.find('img', title=u'点击看大图')['src']
	celebrity.image_url = image_url

	

if __name__ == '__main__':
	get_special('1053560')