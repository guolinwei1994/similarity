# -*- coding: utf-8 -*-

import cherrypy, jieba, gensim

cherrypy.config.update("server.conf")

word_model = gensim.models.Word2Vec.load('model/tag_model')

sent_model = gensim.models.Doc2Vec.load('model/sents2vec_tag_model') 

def add_pos(raw_word):

	if raw_word.endswith(('(a)','(v)','(n)','(u)')):

		return raw_word.decode('utf-8')

	else:

		pos_list = ['(v)','(n)','(a)','(u)']

		word_pos = [raw_word.decode('utf-8') + w for w in pos_list]

		for i in word_pos: 

			if i in word_model.wv.vocab:

				return i

class similar:

	@cherrypy.expose

	def similar_words(self,test_word=None,topn=10,pos=None): 

		try:

			if pos == None:

				sim_words = word_model.most_similar(add_pos(test_word),topn = int(topn))

			else:

				sim_words = [w for w in word_model.most_similar(add_pos(test_word),topn = 200) if w[0].find(pos)>1][:int(topn)]

			results = '\n'.join([w + ':' + str(x) for (w,x) in sim_words])

		except:

			return "error: wrong arguments or word not in vocabulary"

		else:

			return results

	@cherrypy.expose

	def word_similarity(self, word1 = None, word2 = None):

		if word1 == None or word2 == None:

			return "error: need two words to compare"

		else:

			try:

				word_similarity = str(word_model.similarity(add_pos(word1),add_pos(word2)))

			except:

				return "error: wrong arguments or word not in vocabulary"

			else:

				return word_similarity

	@cherrypy.expose

	def sent_similarity(self, sent1=None, sent2=None):

		if sent1 == None or sent2 == None:

			return "error: need two sentences to compare"

		else:

			try:

				sent_list1, sent_list2 = jieba.lcut(sent1.decode('utf-8')), jieba.lcut(sent2.decode('utf-8'))

				similarity_list = []

				for i in range(1,300):

					similarity_list.append(sent_model.docvecs.similarity_unseen_docs(sent_model, sent_list1, sent_list2))

				sent_similarity = str(sum(similarity_list)/len(similarity_list))

				

			except:

				return "error: wrong arguments"

			else:

				return sent_similarity
		


	@cherrypy.expose

	def default(self,*args):

		return "error: input wrong, no such function";

cherrypy.quickstart(similar())
