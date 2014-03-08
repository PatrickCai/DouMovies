#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

import loved
import collected
from spider import get_soup


from role.celebrity  import Celebrity
from role.movie import Movie
from doulist.doulist import Doulist, Celebrities_list, Movie_list

reload(sys)
sys.setdefaultencoding('utf-8')
def merge_the_celebrities():

	star_celebrities = loved.star_celebrities.add(collected.celebrities)
	star_celebrities = sorted(star_celebrities, key=lambda x:x.original_score, reverse=True)

	low_number = 0
	for celebrity in star_celebrities:
		if celebrity.original_score == 2:
			celebrity.final_score = 4
			low_number += 1
		elif celebrity.original_score == 3:
			celebrity.final_score = 5
			low_number += 1

	high_number = len(star_celebrities) - low_number
	for start_number, celebrity in enumerate(star_celebrities):
		if start_number in range(0, high_number/3):
			celebrity.final_score = 7
		elif start_number in range(high_number/3, high_number):
			celebrity.final_score = 6



	# for star_celebrity in star_celebrities:
	# 	print('id:%s final:%s original%s movie %s' %(star_celebrity.ID, star_celebrity.final_score, 
	# 												 star_celebrity.original_score, star_celebrity.movie_loved))
	return star_celebrities
	print(len(star_celebrities))


def merge_the_movies(movie_list):
	movie_list = sorted(movie_list, key=lambda x:x.original_score, reverse=True)
	movie_list = movie_list[0:200]#Only choose the front 200!

	for number, movie in enumerate(movie_list):
		movie_star = unicode(movie.star)
		try:
			star = float(movie_star)/10
		except ValueError:
			star = 0
		bonus_score = 20 - number * 20 / len(movie_list)
		movie.final_score = (1+star) * (80+bonus_score)

	movie_list = Movie_list(set(movie_list)-set(loved.movies_have_seen)) 
	movie_list = sorted(movie_list, key=lambda x:x.final_score, reverse=True)

	#delete all the meanless movies
	return movie_list





