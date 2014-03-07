#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

from spider import get_soup

from role.celebrity  import Celebrity
from role.movie import Movie
from doulist.doulist import Doulist, Celebrities_list

import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')

def get_movies_pages(username, star):
	def is_exist(pages):
		start_number = (pages-1) * 30
		url = 'http://movie.douban.com/people/%s/collect?&rating=%s&mode=list&start=%s'%(username, star, start_number)
		page_soup = get_soup(url)
		content = page_soup.find('li', id=re.compile('list\d{7}'))
		has_found = (True if content else False)
		return has_found
	url = 'http://movie.douban.com/people/%s/collect?&rating=%s&mode=list'%(username, star)
	soup = get_soup(url)
	title_text = soup.title.text
	movies_pages = (int(re.search('\((\d+)\)', title_text).group(1))/30 + 1)*30
	# first_page = 1
	# last_page = movies_pages
	# current_pages = (last_page + 1)/2
	# while ((current_pages != first_page) and (current_pages != last_page)):
	# 	has_found = is_exist(current_pages)
	# 	if has_found:
	# 		first_page = current_pages
	# 		current_pages = (first_page + last_page) / 2
	# 	else:
	# 		last_page = current_pages
	# 		current_pages = (first_page + last_page) / 2
	# current_pages_number = current_pages * 30
	return movies_pages

four_star_movies_IDs = Doulist()
five_star_movies_IDs = Doulist()
def get_movies(username, star, start_number):
	url = 'http://movie.douban.com/people/%s/collect?start=%s&rating=%s&mode=list'%(username, start_number, star)
	soup = get_soup(url)
	htmls = soup.findAll('li', id=re.compile('list\d{7,8}'),  class_=re.compile('item')) 
	page_movies = [re.search('(\d{7,8})', html['id']).group() for html in htmls]
	print('%s start_number OK'%(start_number))
	if star == '4':
		four_star_movies_IDs.extend(page_movies)
	else:
		five_star_movies_IDs.extend(page_movies)


star_celebrities = Celebrities_list()
star_directors = Celebrities_list()
def get_celebrities(username, star, star_movie_ID):
	url = 'http://movie.douban.com/subject/%s/'%(star_movie_ID)
	soup = get_soup(url)
	#celebrity
	celebrity_htmls = soup.findAll('a', {'rel':'v:starring'}, href=re.compile('/celebrity/\d{7}'), limit=4)
	page_celebrity_IDs = [re.search('(\d{7})', celebrity_html['href']).group() for celebrity_html in celebrity_htmls]
	#TODO!the directors are not included!
	directors_htmls = soup.findAll('a', {'rel':'v:directedBy'}, href=re.compile('/celebrity/\d{7}'))
	directors_IDs = [re.search('(\d{7})', directors_html['href']).group() for directors_html in directors_htmls]
	page_celebrities = [Celebrity(page_celebrity_ID, original_score=star) for page_celebrity_ID in page_celebrity_IDs]
	#movie information
	movie_name =soup.find('span', {'property':'v:itemreviewed'}).text 
	movie = Movie(star_movie_ID, movie_name)
	for page_celebrity in page_celebrities:
		page_celebrity.add_loved_movie(movie) 

	star_celebrities.extends(page_celebrities, movie, star)
	print('OK %s movie ID'%(star_movie_ID))


if __name__ == '__main__':
	get_celebrities('cliffedge', '4', '7152895')
