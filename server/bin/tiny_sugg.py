#coding=utf-8

"""
	@Brief build index of suggestion
	@Author wmd
	@Create 2015.11.05
"""

import sugg_conf
import sys

class SuggServer:

	_h_tid2item = {}
	_h_key2item = {}
	_h_prefix2tids = {}

	def load_item_set(self):
		'''
		load item-set
		'''
		ifilename = sugg_conf.FileOutputItemSet

		sys.stderr.write('[trace] begin to build item-set from:%s\n' % (ifilename))

		try:
			ifile = open(ifilename, 'r')
		except:
			sys.stderr.write('[ERROR] cannot open file:%s\n' % ifilename)
			sys.exit(-1)

		line_no = 0
		for line in ifile:
			line_no += 1
			fields = line.replace('\n', '').split('\t')
			if len(fields) != 4:
				sys.stderr.write('[ERROR] invalid fields-count:%d, not %d\n' % (len(fields), 4))
				sys.exit(-1)

			tid = int(fields[0])
			text = fields[1]
			score = int(fields[2])
			att = fields[3]

			item = {
				'tid' : tid,
				'text' : text,
				'score' : score,
				'att' : att,
			}

			key = '%s\t%s' % (text, att)

			self._h_tid2item[tid] = item
			self._h_key2item[key] = item

		ifile.close()
		sys.stderr.write('[trace] done:%s, %d lines\n' % (ifilename, line_no))

	def load_prefix_index(self):
		'''
		load prefix-index-dict
		'''
		ifilename = '%s.prefix' % sugg_conf.FileOutput

		sys.stderr.write('[trace] begin to load prefix-index from:%s\n' % (ifilename))

		try:
			ifile = open(ifilename, 'r')
		except:
			sys.stderr.write('[ERROR] cannot open file:%s\n' % ifilename)
			sys.exit(-1)

		line_no = 0
		for line in ifile:
			line_no += 1
			fields = line.replace('\n', '').split('\t')
			if len(fields) < 2:
				sys.stderr.write('[ERROR] invalid fields-count:%d, < %d\n' % (len(fields), 2))
				sys.exit(-1)

			prefix = fields[0]
			tids = []
			for i in range(1, len(fields)):
				tids.append(int(fields[i]))

			self._h_prefix2tids[prefix] = tids

		ifile.close()
		sys.stderr.write('[trace] done:%s, %d lines\n' % (ifilename, line_no))

	def load_index(self):
		'''
		load index-dicts
		'''
		self.load_item_set()
		self.load_prefix_index()


	def get_sugg(self, prefix):
		'''
		get suggestion-list according to a certain prefix
		'''
		sugg_info = {}
		sugg_info['prefix'] = prefix
		sugg_info['sugg'] = []

		if len(prefix) == 0:
			return sugg_info

		if not prefix in self._h_prefix2tids:
			return sugg_info

		tids = self._h_prefix2tids[prefix]
		for tid in tids:
			if not tid in self._h_tid2item:
				continue

			item = self._h_tid2item[tid]
			sugg_item = {
				'text'  : item['text'],
				'score' : item['score'],
				'att'   : item['att'],
			}
			sugg_info['sugg'].append(sugg_item)

		return sugg_info

	def init(self):
		'''
		init
		'''
		sys.stderr.write('[trace] init\n')

		self.load_index()

	def run(self):
		'''
		dispatch commands
		'''
		if len(sys.argv) < 2:
			sys.stderr.write('[ERROR] no command\n')
			sys.exit(-1)

		sys.stderr.write('[trace] begin to run command: %s\n' % sys.argv[1])

		if sys.argv[1] == 'build_item_set':
			self.build_item_set()
		elif sys.argv[1] == 'gen_tag2tid':
			self.load_item_set()
			self.gen_tag2tid()
		elif sys.argv[1] == 'gen_prefix2tid':
			self.gen_prefix2tid()
		else:
			sys.stderr.write('[ERROR] unknown command: %s\n' % sys.argv[1])
			sys.exit(-1)

		sys.stderr.write('[trace] done.\n')

if __name__ == '__main__':
	server = SuggServer()

	server.init()
	server.run()

