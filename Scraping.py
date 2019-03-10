#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import time
import urllib3
import requests
from bs4 import BeautifulSoup
import re

sys.path.append(os.path.dirname(__file__))
from util.Util import *

class Scraping:

    def __init__(self):
        self.url = None
        self.soup = None

    def parseHtml(self, url):
        '''
        指定されたURLのHTMLをParseする関数
        '''
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content, "lxml")

    def getText(self):
        '''
        HTMLの解析結果からテキスト部分を抽出する関数
        '''
        text = self.soup.text.replace(" ", "").replace("\n", "")
        text = re.sub("[a-zA-Z0-9_]+", "", text)
        text = re.sub("[!-/:-@[-`{-~]+", "", text)
        return text

