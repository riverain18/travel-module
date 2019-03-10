#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import MeCab
import re

sys.path.append(os.path.dirname(__file__))
from Word import *

class MeCabUtil:

    def __init__(self):
        self.path = None
        self.word_obj_list = []


    def getWords(self, string):

        # parseがnoneになるときある
        result = MeCab.Tagger("--eos-format="" ").parse(string)

        lines = result.split("\n")
        del lines[len(lines) - 1]

        # pattern1: 数字、固有名詞以外 / pattern2: 数字、固有名詞
        pattern1 = r"^(.*?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$"
        pattern2 = r"^(.*?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$"

        for line in lines:
            # pattern1の場合
            if re.match(pattern1, line):
                iterator = re.finditer(pattern1, line)
                for i in iterator:
                    surface = i.group(1)
                    pos = i.group(2)
                    base = i.group(8)

            # pattern2の場合
            else:
                iterator = re.finditer(pattern2, line)
                for i in iterator:
                    surface = i.group(1)
                    pos = i.group(2)
                    base = i.group(8)

            # 原形がない場合は表層単語を使用
            if base == "*":
                base = surface

            # Word Objectを作成
            word_obj = Word(surface, pos, base)

            # Word Objectのリストに追加
            self.word_obj_list.append(word_obj)

        return self.word_obj_list


instance=MeCabUtil()
instance.getWords("今日は晴れです")
