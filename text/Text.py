#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import re

sys.path.append(os.path.dirname(__file__))
from MeCabUtil import *

class Text:

    def __init__(self, string, stopwords):
        self.path = None
        self.str = string
        # self.words = None
        self.words_cache = None
        self.stopwords = stopwords

    def __len__(self):
        '''
        文書長を返す関数
        '''
        return len(self.words())

    def text(self):
        '''
        文書を返す関数
        '''
        return self.str

    def words(self, content_pos=["名詞"]):
        '''
        文書を分かち書きしたリストを返す関数
        '''
        # wordsのキャッシュがない場合は、分かち書きを実行
        if self.words_cache is None:
            self.words_cache = MeCabUtil().getWords(self.str)

            if content_pos == []:
                self.words_cache = [word.base for word in self.words_cache]
            else:
                self.words_cache = [word.base for word in self.words_cache  if word.pos in content_pos]

            ### ストップワード除去 ###
            self.words_cache = self.remove_stopwords(self.words_cache)
        return self.words_cache

    def remove_stopwords(self, words):
        '''
        ストップワードを除去する関数
        '''
        # 単語長
        words = [word for word in words if len(word) >= 2]
        # 一般的なストップワード
        words = [word for word in words if word not in self.stopwords]
        # 数字
        words = [word for word in words if re.search("\D+", word)]
        # ひらがな二文字
        words = [word for word in words if re.search("[ぁ-ん]{2}", word) is None]
        # ひらがな、カタカナ、漢字以外
        # words = [word for word in words if re.search("[^一-龥ぁ-んァ-ン]+", word) is None]

        return words


class TextCollection:

    def __init__(self, slist):
        self.path = None
        self.slist = slist
        #self.tlist = None
        self.tlist_cache = None
        # self.words_list = []
        self.stopwords = []
        self.loadStopWords()
 
    def loadStopWords(self):
        f = open(os.path.dirname(__file__) + "/stopwords_list.txt", "r")
        lines = f.readlines()
        for line in lines:
            self.stopwords.append(line.replace("\n", ""))

    def __len__(self):
        '''
        Text Objectの数を返す関数
        '''
        return len(self.tlist())

    def tlist(self):
        '''
        Text Objectのリストを返す関数
        '''
        if self.tlist_cache is None:
            self.tlist_cache = [Text(string, self.stopwords) for string in self.slist]
        return self.tlist_cache

    def words_list(self, content_pos=["名詞"]):
        '''
        Text Objectから得られるwordsのリストを返す関数
        '''
        return [text_obj.words(content_pos) for text_obj in self.tlist()]


    def vocab(self, content_pos=["名詞"]):
        '''
        Vocab(ユニーク単語リスト)を返す関数
        '''
        vocab = sum(self.words_list(content_pos), [])
        return list(set(vocab))


