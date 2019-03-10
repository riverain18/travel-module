#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from sklearn.cluster import KMeans
import numpy as np
import copy

sys.path.append(os.path.dirname(__file__))
from text.TFIDF import *
from text.Word2Vec import *

class Test:
    def __init__(self, obj):
        print(obj.vocab())

class TFIDFCluster(TFIDF):

    def __init__(self, obj):
        super(TFIDFCluster, self).__init__(obj)
        self.path = None
        self.data = None
        self.kmeans = None
        self.vec_list = None


    def getFormatFeature(self):
        '''
        整形した特徴量を取得する関数
        '''
        if self.vec_list is None:
            self.vec_list = self.formatFeature()
        return self.vec_list


    def formatFeature(self):
        '''
        特徴量を整形する関数
        '''
        format_list = []

        # 辞書ベクトル作成
        vocab_vec = {}
        for word in self.tc.vocab():
            vocab_vec[word] = 0.0

        for tup in self.tfidf():
            vec = {}
            vec_val = []
            vec = copy.copy(vocab_vec)
            for word, val in tup.vec.items():
                vec[word] = val
            for word, val in sorted(vec.items(), key=lambda x: x[0]):
                vec_val.append(val)
            format_list.append(vec_val)
        return np.array(format_list)



    def fitKmeans(self, n_clusters, random_state=0):
        '''
        Kmeansを実行する関数
        '''
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state).fit(self.getFormatFeature())
        print(self.kmeans.labels_)




class W2VCluster:

    def __init__(self, obj):
        self.tfidf_obj = TFIDF(obj)
        self.w2v_obj = Word2Vec(obj)
        self.path = None
        self.data = None
        self.kmeans = None
        self.vec_list = None

        self.top_word_list = []


    def getFormatTFIDFFeature(self):
        '''
        整形した特徴量を取得する関数
        '''
        if self.vec_list is None:
            self.vec_list = self.formatFeature()
        return self.vec_list


    def getFormatW2VFeature(self):
        '''
        整形したWord2Vecの特徴量を取得する関数
        '''
        if self.vec_list is None:
            self.vec_list = self.formatW2VFeature()
        return self.vec_list


    def formatTFIDFFeature(self):
        '''
        特徴量を整形する関数
        '''
        format_list = []

        # 辞書ベクトル作成
        vocab_vec = {}
        for word in self.tfidf_obj.tc.vocab():
            vocab_vec[word] = 0.0

        for tup in self.tfidf_obj.tfidf():
            vec = {}
            vec_val = []
            vec = copy.copy(vocab_vec)
            for word, val in tup.vec.items():
                vec[word] = val
            for word, val in sorted(vec.items(), key=lambda x: x[0]):
                vec_val.append(val)
            format_list.append(vec_val)
        return np.array(format_list)


    def formatW2VFeature(self):
        format_list = []
        for tup in self.tfidf_obj.tfidf():
            try:
                top_word = max(tup.vec, key=tup.vec.get)
            except:
                print(tup.text.text())
                print(tup.vec)
                sys.exit()
            print(top_word)
            self.top_word_list.append(top_word)
            format_list.append(self.w2v_obj.getWordVec(top_word))
        return format_list


    def fitKmeans(self, n_clusters, random_state=0):
        '''
        Kmeansを実行する関数
        '''
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state).fit(self.getFormatW2VFeature())
        print(self.kmeans.labels_)


    def outputResult(self, n_clusters):
        for cluster_num in range(n_clusters):
            print("\n====== {0} ======".format(cluster_num))
            for i, label in enumerate(self.kmeans.labels_):
                if label == cluster_num:
                    print(self.top_word_list[i])
                    print(self.tfidf_obj.tc.tlist()[i].text())
                    print("----------------------")

