#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from math import log
import numpy as np

from collections import namedtuple
TextVec = namedtuple('TextVec', ('text', 'vec'))

sys.path.append(os.path.dirname(__file__))
from Feature import *

class TFIDF(Feature):

    def __init__(self, tc):
        super(TFIDF, self).__init__(tc)
        self.tf_vecs = None
        self.idf_vecs = None
        self.tfidf_vecs = None
        self.feature = None


    def calcTF(self, word, text, normalize=True):
        '''
        TFを計算する関数
        '''
        if normalize:
            return float(text.count(word)) / float(len(text))
        else:
            return float(text.count(word))


    def calcTFVec(self, text, normalize=True):
        '''
        TF Vectorを計算する関数
        input : text
        output : vector
        '''
        tf_vec = {}
        for word in text:
            tf_vec[word] = tf_vec.get(word, 0) + 1.0

        if normalize:
            return {key:(float(val)/float(len(text))) for key, val in tf_vec.items()}
        else:
            return tf_vec


    def calcIDF(self, word):
        '''
        IDFを計算する関数
        '''
        if self.idf_vecs is None:
            df = len([True for text in self.tc.words_list() if word in text])
            idf = (log(float(len(self.tc.words_list())) / df) if df else 0.0)
            return idf
        else:
            return self.idf_vecs[word]

    def calcIDFVec(self):
        '''
        IDF Vectorを計算する関数
        '''
        if self.idf_vecs is None:
            self.idf_vecs = {}
            for word in tc.vocab():
                self.idf_vecs[word] = self.calcIDF(word)
        return self.idf_vecs


    def calcTFIDF(self, word, text):
        '''
        TF-IDFを計算する関数
        '''
        return self.calcTF(word, text) * self.calcIDF(word)


    def tf(self, normalize=True):
        '''
        TFの結果を返す関数
        '''
        if self.tf_vecs is None:
            self.tf_vecs = []
            for text_obj in self.tc.tlist():
                tf_vec = {}
                tf_vec = self.calcTFVec(text_obj.words(), normalize)
                self.tf_vecs.append(TextVec(text_obj, tf_vec))
        return self.tf_vecs


    def idf(self):
        '''
        IDFの結果を返す関数
        '''
        return self.calcIDFVec()


    def tfidf(self):
        '''
        TF-IDFの結果を返す関数
        '''
        if self.tfidf_vecs is None:
            self.tfidf_vecs = []
            for text_obj in self.tc.tlist():

                tfidf_vec = {}
                for word in text_obj.words():
                    tfidf_vec[word] = self.calcTFIDF(word, text_obj.words())

                self.tfidf_vecs.append(TextVec(text_obj, tfidf_vec))
        return self.tfidf_vecs


    def formatVecsForKmeans(self):
        '''
        TF-IDFベクトルを、Kmeansの特徴量に整形する関数
        '''
        # 辞書ベクトル作成
        vocab_vec = {}
        for word in self.tc.vocab():
            vocab_vec[word] = 0.0

        tfidf_vecs_format = []
        for tfidf in self.tfidf():

            # ベクトル値を設定
            vec = vocab_vec
            vec_val_list = []
            for word, val in tfidf.vec.items():
                vec[word] = val
            for word, val in sorted(vec.items(), key=lambda x: x[0]):
                vec_val_list.append(val)
            tfidf_vecs_format.append(TextVec(tfidf.text, vec_val_list))

        return tfidf_vecs_format



    def getFeature(self):
        '''
        特徴量(TF-IDF)を返す関数
        '''
        # if self.feature is None:
        #     self.feature = self.formatVecsForKmeans()
        # return self.feature
        return self.tfidf()


    def calcFeature(self):
        '''
        特徴量(TF-IDFベクトル)を算出する関数
        '''
        pass



