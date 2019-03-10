#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os


class Word:
    def __init__(self, surface, pos, base):
        self.surface = surface
        self.pos = pos
        self.base = base

    def getSurface(self):
        return self.surface

    def getPos(self):
        return self.pos

    def getBase(self):
        return self.base
