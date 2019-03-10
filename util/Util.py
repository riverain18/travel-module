#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import csv
import json

class Util:

    def __init__(self, load_data_path, write_data_path):
        self.load_data_path = load_data_path
        self.write_data_path = write_data_path

    def writeJson(self, json_data, file_name):
        '''
        JsonデータをJsonファイルに書き込む関数
        '''
        fw = open("{0}/{1}".format(self.write_data_path, file_name), "w")
        json.dump(json_data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        fw.close()

    def loadJson(self, file_name):
        '''
        Jsonファイルを読み込む関数
        '''
        f = open("{0}/{1}".format(self.load_data_path, file_name), "r")
        json_data = json.load(f)
        f.close()
        return json_data

    def loadCsv(self, file_name):
        '''
        csvファイルを読み込む関数
        '''
        csv_data = []
        f = open("{0}/{1}".format(self.load_data_path, file_name), "r")
        reader = csv.reader(f)
        for row in reader:
            csv_data.append(row)
        f.close()
        return csv_data


    def loadJsonFree(self, data_path, file_name):
        '''
        Jsonファイルを読み込む関数
        Path Free
        '''
        f = open("{0}/{1}".format(data_path, file_name), "r")
        json_data = json.load(f)
        f.close()
        return json_data


    def writeTextFree(self, data_path, text_data, file_name):
        '''
        Textファイルに書き込む関数
        Path Free
        '''
        f = open("{0}/{1}".format(data_path, file_name), "w")
        f.write(text_data)
        f.close()


    def writeJsonFree(self, data_path, json_data, file_name):
        '''
        JsonデータをJsonファイルに書き込む関数
        Path Free
        '''
        fw = open("{0}/{1}".format(data_path, file_name), "w")
        json.dump(json_data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        fw.close()



