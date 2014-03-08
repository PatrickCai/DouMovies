#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import time

import gevent
import spider.collected as collected
import spider.loved as loved
import spider.merge as merge
import spider.recommend as recommend
import cPickle

reload(sys)
sys.setdefaultencoding('utf-8')


username = 'cliffedge'

def get_celebrities_spawns():
	pages = collected.get_celebrities_pages(username)
	spawns = [gevent.spawn(collected.get_celebrities, username, start_number) for start_number in xrange(0, pages, 15)]
	return spawns

def get_loved_movies_spawns():
	total_pages = loved.get_movies_pages(username)
	total_spawns = [gevent.spawn(loved.get_movies, username, start_number) for start_number in xrange(0, total_pages, 30)]
	return total_spawns

def get_loved_celebrities_spawns():
	def get_star_spawns(star):

		if star == '4':
			star_movies_IDs = loved.four_star_movies_IDs
		else:
			star_movies_IDs = loved.five_star_movies_IDs
		spawns = [gevent.spawn(loved.get_celebrities, username, star, star_movies_ID) for star_movies_ID in star_movies_IDs]
		return spawns

	four_spawns = get_star_spawns('4')
	five_spawns = get_star_spawns('5')
	total_spawns = five_spawns + four_spawns
	return total_spawns

def get_recommendation_movies_spawns(star_celebrities, page):
	page_number = {"1":0, '2':25, '3':50}
	choose_celebrities = {'1':star_celebrities[0:200], '2':recommend.second_page_celebrities, '3':recommend.third_page_celebrities}
	celebrities = choose_celebrities[page]
	start_number = page_number[page]
	celebrities_spawns = [gevent.spawn(recommend.get_movies, username, celebrity, start_number) for celebrity in celebrities]
	return celebrities_spawns



if __name__ == '__main__':
	beginning_time = time.time()
	cele_spawns=get_celebrities_spawns()
	gevent.joinall(cele_spawns)
	print('Get all the collected movie stars')

	loved_moview_spawns = get_loved_movies_spawns()
	gevent.joinall(loved_moview_spawns)
	print('Get all the loved movies')

	loved_celebrities_spawns = get_loved_celebrities_spawns()
	gevent.joinall(loved_celebrities_spawns)
	print('Get all the loved movie stars')


	star_celebrities = merge.merge_the_celebrities()
	print('Merged the celebrities')

	# cPickle.dump(star_celebrities, open('yes', 'w'))
	# star_celebrities=cPickle.load(open('yes', 'r'))

	recommendation_movies_spawns = get_recommendation_movies_spawns(star_celebrities, "1")
	gevent.joinall(recommendation_movies_spawns)
	second_page_spawns = get_recommendation_movies_spawns(star_celebrities, '2')
	print len(second_page_spawns)
	gevent.joinall(second_page_spawns)
	third_page_spawns = get_recommendation_movies_spawns(star_celebrities, '3')
	print len(third_page_spawns)
	gevent.joinall(third_page_spawns)
	print('Get all the recommendation movies')



	movie_list = merge.merge_the_movies(recommend.movie_list)
	for movie in movie_list:
		print('Movie ID %s name %s final_score %s'%(movie.ID, movie.name, movie.final_score))
		for celebrity in movie.celebrities:
			print(celebrity.name)

	end_time = time.time()
	passing_time = end_time - beginning_time
	print('Pass %s mins'%(int(passing_time)/60))
