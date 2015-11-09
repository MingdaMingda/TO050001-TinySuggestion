#coding=utf-8

"""
	@Brief build index of suggestion
	@Author wmd
	@Create 2015.11.05
"""

import sugg_conf
import sys

from pypinyin import lazy_pinyin

class SuggIndexer:

	_h_tid2item = {}
	_h_key2item = {}

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

	def build_item_set(self):
		'''
		build item-set
		'''
		ifilename = sugg_conf.FileInput

		sys.stderr.write('[trace] begin to build item-set from:%s\n' % (ifilename))

		try:
			ifile = open(ifilename, 'r')
		except:
			sys.stderr.write('[ERROR] cannot open file:%s\n' % ifilename)
			sys.exit(-1)

		tid = 0
		h_key = {}
		h_text = {}

		line_no = 0
		for line in ifile:
			line_no += 1
			fields = line.replace('\n', '').split('\t')
			if len(fields) < 3:
				sys.stderr.write('[ERROR] invalid fields-count:%d, less then %d\n' % (len(fields), 3))
				sys.exit(-1)

			text = fields[0]
			score = int(fields[1])
			taglist = fields[2]
			att = ''
			if len(fields) == 4:
				att = fields[3]

			### check text
			if len(text) == 0:
				sys.stderr.write('[WARN] blank text, Skip: %d, %s' % (line_no, line))
				continue

			key = '%s\t%s' % (text, att)
			if key in h_key:
				sys.stderr.write('[WARN] duplicated text, Skip: %d, %s' % (line_no, line))
				continue

			if sugg_conf.ifMergeSampleText == 1:
				if key in h_text:
					continue

			h_key[key] = 1
			h_text[text] = 1

			sys.stdout.write('%d\t%s\t%d\t%s\n' % (tid, text, score, att))
			tid += 1

		ifile.close()
		sys.stderr.write('[trace] done:%s, %d lines, %d texts\n' % (ifilename, line_no, tid))

	def gen_tag2tid(self):
		'''
		generate tag2tid
		'''
		ifilename = sugg_conf.FileInput

		sys.stderr.write('[trace] begin to generate tag2tid:%s\n' % (ifilename))

		try:
			ifile = open(ifilename, 'r')
		except:
			sys.stderr.write('[ERROR] cannot open file:%s\n' % ifilename)
			sys.exit(-1)

		h_key = {}
		h_text = {}

		line_no = 0
		tag_no = 0
		for line in ifile:
			line_no += 1
			fields = line.replace('\n', '').split('\t')
			if len(fields) < 3:
				sys.stderr.write('[ERROR] invalid fields-count:%d, less then %d\n' % (len(fields), 3))
				sys.exit(-1)

			text = fields[0]
			score = fields[1]
			taglist = fields[2]
			att = ''
			if len(fields) == 4:
				att = fields[3]

			key = '%s\t%s' % (text, att)
			if not key in self._h_key2item:
				sys.stderr.write('[WARN] not in item-set, Skip: %d, %s' % (line_no, line))
				continue

			item = self._h_key2item[key]

			tags = taglist.split('|')

			for tag in tags:
				if len(tag) > 0:
					sys.stdout.write('%s\t%d\t%s\t%s\n' % (tag, item['tid'], score, 1))
					tag_no += 1

			if sugg_conf.ifFullText == 1:
				sys.stdout.write('%s\t%d\t%s\t%s\n' % (text, item['tid'], score, 0))
				tag_no += 1

		ifile.close()
		sys.stderr.write('[trace] done:%s, %d lines, %d tags\n' % (ifilename, line_no, tag_no))

	def expand_tag(self, tag):
		'''
		expand tag by pinyin etc.
		'''
		tags = [tag]

		if sugg_conf.ifPinYin == 1:
			tags = self.expand_tag_by_pinyin(tag, tags)

		return tags

	def get_prefix_list(self, tag):
		'''
		generate prefix-list of a tag
		'''
		tag_unicode = tag.decode(sugg_conf.encoding)

		tags = self.expand_tag(tag_unicode)

		sys.stdout.write('tags:%s\n' % ('|'.join(tags)).encode(sugg_conf.encoding))

		prefix_list = []

		for i in range(0, len(tags)):
			for j in range(1, len(tags[i]) + 1):
				prefix_list.append(tags[i][0:j].encode(sugg_conf.encoding))

		return prefix_list

	def expand_tag_by_pinyin(self, tag, tags):
		'''
		get pinyin of a tag
		'''
		py = lazy_pinyin(tag)

		if sugg_conf.ifPinYin == 1:
			py_str = ''.join(py)
			tags.append(py_str)

		if sugg_conf.ifJianPin == 1:
			jp_str = ''
			for i in range(0, len(py)):
				jp_str = '%s%s' % (jp_str, py[i][0])
			tags.append(jp_str)

		return tags

	def gen_prefix2tid(self):
		'''
		generate input-prefix
		'''
		ifilename = sugg_conf.FileTag2tid

		sys.stderr.write('[trace] begin to generate tag2tid:%s\n' % (ifilename))

		try:
			ifile = open(ifilename, 'r')
		except:
			sys.stderr.write('[ERROR] cannot open file:%s\n' % ifilename)
			sys.exit(-1)

		h_key = {}
		h_text = {}

		line_no = 0
		tag_no = 0
		for line in ifile:
			line_no += 1
			fields = line.replace('\n', '').split('\t')
			if len(fields) != 4:
				sys.stderr.write('[ERROR] invalid fields-count:%d, not %d\n' % (len(fields), 2))
				sys.exit(-1)

			tag = fields[0]
			tid = fields[1]
			score = fields[2]
			mode = fields[3]

			prefix_list = self.get_prefix_list(tag)
			for prefix in prefix_list:
				sys.stdout.write('%s\t%s\t%s\t%s\t%s\n' % (prefix, tid, score, mode, tag))

		ifile.close()
		sys.stderr.write('[trace] done:%s, %d lines, %d tags\n' % (ifilename, line_no, tag_no))

	def init(self):
		'''
		init
		'''
		sys.stderr.write('[trace] init\n')

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
	indexer = SuggIndexer()

	indexer.init()
	indexer.run()

