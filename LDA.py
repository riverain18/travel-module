#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import gensim
from gensim import corpora, models, similarities

sys.path.append(os.path.dirname(__file__))
from text.TFIDF import *
from text.Word2Vec import *
from text.Text import *

class LDA:

    def __init__(self, tc):
        # super(LDA, self).__init__(tc)
        self.tc = tc
        self.dictionary = None
        self.corpus = []
        self.model = None


    def makeDictionary(self):
        '''
        辞書を作成する関数
        '''
        # 辞書(単語と出現回数のペア)を作成
        self.dictionary = corpora.Dictionary(self.tc.words_list())

        # 辞書にフィルタをかける
        self.dictionary.filter_extremes(no_below=10, no_above=0.5)

        self.dictionary.save_as_text(os.path.dirname(__file__) + "/../model/dict.txt")


    def makeBoWCorpus(self):
        '''
        BoWコーパスを作成する関数
        '''
        corpus = [self.dictionary.doc2bow(words) for words in self.tc.words_list()]


    def makeLDAModel(self, num_topics=4):
        '''
        LDAモデルを作成する関数
        '''
        if self.dictionary is None:
            self.makeDictionary()

        if len(self.corpus) == 0:
            self.makeBoWCorpus()

        self.model = models.ldamodel.LdaModel(
            corpus=self.corpus,
            num_topics=num_topics,
            id2word=self.dictionary)

        for t in range(self.model.num_topics):
            print("=== {0} ===".format(t))
            topic = self.model.show_topic(t)
            print(topic)