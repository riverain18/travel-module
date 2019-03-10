#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from cabocha.analyzer import CaboChaAnalyzer
import re
import gensim

sys.path.append(os.path.dirname(__file__))
from Word import *


class CaboChaUtil:

    def __init__(self):
        self.path = None
        self.word_obj_list = []

    def getWords(self, string):
        result = CaboChaAnalyzer().parse(string)
        print(result)


sentence = "太郎はこの本を二郎を見た女性に渡した。"
obj = CaboChaUtil()
obj.getWords(sentence)