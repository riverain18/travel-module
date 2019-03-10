#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(__file__))


class Config:

    def __init__(self):
        self.LOAD_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../data"
        self.WRITE_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../data"
        self.WRITE_DATA_PATH_DETAIL = os.path.dirname(os.path.abspath(__file__)) + "/../data/detail"
        self.WEB_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../data/web"
