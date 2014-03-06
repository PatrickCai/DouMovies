#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

import loved
import collected
from collections import Counter
from spider import get_soup


from role.celebrity  import Celebrity
from role.movie import Movie


reload(sys)
sys.setdefaultencoding('utf-8')

def merge_the_celebrities():
	star_celebrities = loved.four_star_celebrities + loved.five_star_celebrities + collected.celebrities
	'''merge all the celebrities into one list and make its final socre'''
	four_counter = Counter(collected.celebrities)
	three_counter = Counter(loved.four_star_celebrities)
	two_counter = Counter(loved.five_star_celebrities)

	for star_celebrity in star_celebrities :
		original_score = 0
		original_score += (four_counter[star_celebrity] * 3)
		original_score += (three_counter[star_celebrity] * 3) 
		original_score += (two_counter[star_celebrity] * 2)
		star_celebrity.original_score = original_score		
	#merge the celebrities including the movies involved
	movie_counter = Counter(loved.four_star_celebrities + loved.five_star_celebrities)
	for movie, times in 
	star_celebrities = sorted(set(star_celebrities), key=lambda x:x.original_score, reverse=True)

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




	for star_celebrity in star_celebrities :
		print('id:%s final:%s original%s movie %s' %(star_celebrity.ID, star_celebrity.final_score, 
													 star_celebrity.original_score, star_celebrity.movie_loved))



