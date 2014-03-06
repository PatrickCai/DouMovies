#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys

import gevent
import spider.collected as collected
import spider.loved as loved
import spider.merge as merge
import spider.recommend as recommend

import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')


username = 'cliffedge'

def get_celebrities_spawns():
	pages = collected.get_celebrities_pages(username)
	spawns = [gevent.spawn(collected.get_celebrities, username, start_number) for start_number in xrange(0, pages, 15)]
	return spawns

def get_loved_movies_spawns():
	#first 4 star movie
	#NOT ELEGENT!!merge it into one function
	four_pages = loved.get_movies_pages(username, '4')
	four_spawns = [gevent.spawn(loved.get_movies, username, '4', start_number) for start_number in xrange(0, four_pages, 30)]
	five_pages = loved.get_movies_pages(username, '5')
	five_spawns = [gevent.spawn(loved.get_movies, username, '5', start_number) for start_number in xrange(0, five_pages, 30)]
	total_spawns = five_spawns + four_spawns
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

def get_recommendation_movies_spawns():
	celebrities_spawns = []
	for celebrity in merge.star_celebrities:
		part_celebrities_spawns = [gevent.spawn(recommend.get_movies, username, celebrity.ID, start_number) for start_number in xrange(0, 75, 25)]
		celebrities_spawns.extend(part_celebrities_spawns)

	return celebrities_spawns

if __name__ == '__main__':
	cele_spawns=get_celebrities_spawns()
	gevent.joinall(cele_spawns)
	print('Get all the collected movie stars')

	loved_moview_spawns = get_loved_movies_spawns()
	gevent.joinall(loved_moview_spawns)
	print('Get all the loved movies')

	loved_celebrities_spawns = get_loved_celebrities_spawns()
	gevent.joinall(loved_celebrities_spawns)
	print('Get all the loved movie stars')

	merge.merge_the_celebrities()
	print('Merged the celebrities')

	# recommendation_movies_spawns = get_recommendation_movies_spawns()



