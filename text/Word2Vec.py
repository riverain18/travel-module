#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import gensim
from gensim.models.fasttext import FastText
import numpy as np

sys.path.append(os.path.dirname(__file__))
from Feature import *

class Word2Vec(Feature):

    def __init__(self, tc):
        super(Word2Vec, self).__init__(tc)
        self.model_path = os.path.dirname(__file__) + "/../../model"
        self.model_name = "model"
        self.model = None

    def loadModel(self):
        '''
        Word2Vecの学習済みモデルを読み込む関数
        '''
        if self.model is None:
            self.model = gensim.models.KeyedVectors.load_word2vec_format("{0}/{1}.vec".format(self.model_path, self.model_name), binary=False)
            # self.model = FastText.load_fasttext_format("{0}/{1}".format(self.model_path, self.model_name), full_model=True)
        else:
            pass

    def getWordVec(self, word):
        '''
        単語ベクトルを取得する関数
        '''
        if self.model is None:
            self.loadModel()
        try:
            return self.model.wv[word]
        except:
            return np.zeros(300)


    def getFeature(self):
        '''
        特徴量(TF-IDF)を返す関数
        '''
        pass


    def calcFeature(self):
        '''
        特徴量(TF-IDFベクトル)を算出する関数
        '''
        pass


