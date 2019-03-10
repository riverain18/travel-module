#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from abc import ABCMeta, abstractmethod
import numpy as np

class Feature(object, metaclass=ABCMeta):
    '''
    ベクトル空間モデルの特徴量を管理する抽象クラス
    '''

    def __init__(self, tc):
        self.tc = tc
        self.feature = None

    @abstractmethod
    def getFeature(self):
        '''
        特徴量を返す関数
        '''
        pass

    @abstractmethod
    def calcFeature(self):
        '''
        特徴量を算出する関数
        '''
        pass
