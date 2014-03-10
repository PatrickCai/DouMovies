#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import time

import gevent
import spider.collected as collected
import spider.loved as loved
import spider.merge as merge
import spider.recommend as recommend
import spider.filtered as filtered
import cPickle

reload(sys)
sys.setdefaultencoding('utf-8')


username = 'cliffedge'

def get_celebrities_spawns():
	pages = collected.get_celebrities_pages(username)
	spawns = [gevent.spawn(collected.get_celebrities, username, start_number)
			  			   for start_number 
			  			   in xrange(0, pages, 15)]
	return spawns

def get_loved_movies_spawns():
	total_pages = loved.get_movies_pages(username)
	total_spawns = [gevent.spawn(loved.get_movies, username, start_number) 
					for start_number
					in xrange(0, total_pages, 30)]
	return total_spawns

def get_loved_celebrities_spawns():
	def get_star_spawns(star):
		choose_star = {'4':loved.four_star_movies_IDs,
					   '5':loved.five_star_movies_IDs}
		star_movies_IDs = choose_star[star]
		spawns = [gevent.spawn(loved.get_celebrities, username, star, star_movies_ID)
			      for star_movies_ID in star_movies_IDs]
		return spawns

	four_spawns = get_star_spawns('4')
	five_spawns = get_star_spawns('5')
	total_spawns = five_spawns + four_spawns
	return total_spawns

def get_recommendation_movies_spawns(star_celebrities, page, role='performer'):
	page_number = {"1":0, '2':25, '3':50}
	start_number = page_number[page]
	choose_celebrities = {
						  '1':star_celebrities[0:300], 
						  '2':recommend.second_page_celebrities,
						  '3':recommend.third_page_celebrities
						  }
	celebrities = choose_celebrities[page]
	celebrities_spawns = [gevent.spawn(recommend.get_movies, username, 
						  celebrity, start_number, role)
						  		for celebrity in celebrities]
	return celebrities_spawns

def get_filter_movies_spawns(movie_list):
	movies_spawns= [gevent.spawn(filtered.get_final_movies, movie,) for movie in movie_list]
	return movies_spawns

def get_special_spawns(movies):
	existing_celebrities = []
	spawns = []
	for movie in movies:
		for celebrity in movie.celebrities:
			if celebrity not in existing_celebrities:
				spawns.append(gevent.spawn(filtered.get_special, celebrity))
				existing_celebrities.append(celebrity)

if __name__ == '__main__':
	beginning_time = time.time()
	spawns=get_celebrities_spawns()
	gevent.joinall(spawns)
	print('Get all the collected movie stars')

	spawns = get_loved_movies_spawns()
	gevent.joinall(spawns)
	print('Get all the loved movies')

	spawns = get_loved_celebrities_spawns()
	gevent.joinall(spawns)
	print('Get all the loved movie stars')


	star_celebrities = merge.merge_the_celebrities()
	star_directors = merge.merge_the_directors()
	print('Merged the celebrities')


	for page in range(1,4):
		spawns = get_recommendation_movies_spawns(star_celebrities, '%s'%(page))
		gevent.joinall(spawns)
		print('actor page %s finished!'%(page))


	recommend.second_page_celebrities = recommend.third_page_celebrities = []

	for page in range(1, 4):
		spawns = get_recommendation_movies_spawns(star_directors, '%s'%(page), role='director')	
		gevent.joinall(spawns)
		print("director page %s finished!"%(page))
	print('Get all the recommendation movies')





	movie_list = merge.merge_the_movies(recommend.movie_list)

	filter_movies_spawns = get_filter_movies_spawns(movie_list)
	gevent.joinall(filter_movies_spawns)

	# cPickle.dump(star_celebrities, open('yes', 'w'))
	# star_celebrities=cPickle.load(open('yes', 'r'))

	spawns = get_special_spawns(filtered.final_movies)
	gevent.joinall(spawns)

	for movie in filtered.final_movies:
		print('Movie ID %s name %s final_score %s'%(movie.ID, movie.name, movie.final_score))
		for celebrity in movie.celebrities:
			print('  %s'%(unicode(celebrity.name)))
			print('  %s'%(celebrity.ID))
			print('  %s'%(celebrity.image_url))
			for loved_movie in celebrity.movie_loved:
				print(u'    %s'%(loved_movie.name))

	end_time = time.time()
	passing_time = end_time - beginning_time
	print('Pass %s seconds'%(int(passing_time)))
