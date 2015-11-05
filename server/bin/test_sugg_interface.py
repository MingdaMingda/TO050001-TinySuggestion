#coding=utf-8

"""
	@Brief test suggestion-server interface
	@Author wmd
	@Create 2015.11.05
"""

import sys

from tiny_sugg import SuggServer

def test():
	server = SuggServer()
	server.init()

	prefix = "面"
	sugg_info = server.get_sugg(prefix)

	print sugg_info['prefix']
	for item in sugg_info['sugg']:
		print '\t%s\t%s\t%s' % (item['text'], item['score'], item['att'])


if __name__ == '__main__':
	test()
	
