# -*- coding: utf-8 -*-

import cherrypy, jieba, gensim

cherrypy.config.update("server.conf")

word_model = gensim.models.Word2Vec.load('model/tag_model')

sent_model = gensim.models.Doc2Vec.load('model/sents2vec_tag_model') 

class similar:

	@cherrypy.expose

	def similar_words(self,test_word,topn): 

		sim_words = word_model.most_similar(test_word.decode('utf-8'),topn = int(topn))

		results = '\n'.join([w + ':' + str(x) for (w,x) in sim_words])

		return results

	@cherrypy.expose

	def word_similarity(self, word1, word2):

		word_similarity = str(word_model.similarity(word1.decode('utf-8'),word2.decode('utf-8')))

		return word_similarity

	@cherrypy.expose

	def sent_similarity(self, sent1, sent2):

		sent_similarity = str(sent_model.docvecs.similarity_unseen_docs(sent_model,jieba.lcut(sent1.decode('utf-8')),jieba.lcut(sent2.decode('utf-8'))))

		return sent_similarity
		


	@cherrypy.expose

	def default(self, year, month, day,aa):

		return "error";

cherrypy.quickstart(similar())
