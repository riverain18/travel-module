#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import csv
import json
import re

sd = os.path.dirname(__file__)
sys.path.append(sd)
from util.Util import Util

class PublicCloud:

    def __init__(self, load_data_path, write_data_path):
        self.load_data_path = load_data_path
        self.write_data_path = write_data_path

        self.csv_data = []
        self.json_data = {}

        # 観光地名
        self.name_list = []
        self.name_dic = {}

        # データ読み書き関連
        self.util = Util(load_data_path=self.load_data_path, write_data_path=self.write_data_path)


    def writeJson(self, file_name, json_data):
        '''
        jsonデータをjsonファイルに書き込む関数
        '''
        fw = open("{0}/{1}.json".format(self.data_path, file_name), "w")
        json.dump(json_data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


    def loadCSV(self, file_name):
        '''
        csvファイルを読み込む関数
        '''
        f = open("{0}/{1}.csv".format(self.data_path, file_name), "r")
        reader = csv.reader(f)
        for row in reader:
            self.csv_data.append(row)


    def formatCsvToJson(self):
        '''
        公共クラウドシステムのCSVファイルをJsonファイルに整形する関数
        '''

        tourspots_num = 0
        tourspots_num_cache = 0
        json_tmp = {}
        cnt = 0
        for i, row in enumerate(self.csv_data):

            # tourspots[]の番号を抽出
            searchOb = re.search("\d+", row[0])
            if searchOb:
                tourspots_num = int(searchOb.group())
            else:
                sys.exit()

            # 空白の要素とtourspots[]の要素を削除
            row = list(filter(lambda a: a != "", row))
            row.pop(0)

            # tourspots[]の番号が変わった場合
            if tourspots_num != tourspots_num_cache:
                # ここまでの情報をJsonデータとして保存
                self.json_data[tourspots_num_cache] = json_tmp
                json_tmp = {}
                print("=== {0} ===".format(cnt))
                cnt += 1

            # name の判定
            if row[0] == "name" and row[2] == "written":
                json_tmp["name"] = row[len(row)-1]

            # visit の判定
            if row[0] == "descs[0]":
                json_tmp["description"] = row[len(row)-1]

            # genre の判定
            if row[0] == "genres[0]":
                json_tmp["genre{0}".format(row[1])] = row[len(row)-1]

            # tourspots[]の番号をキャッシュ
            tourspots_num_cache = tourspots_num

        self.util.writeJson(json_data=self.json_data, file_name="kanko_all_format.json")

    def makeNameDump(self):
        '''
        観光地名だけのDumpファイルを作成する関数
        '''
        pass

"""
data_path = os.path.dirname(os.path.abspath(__file__)) + "/../data"
instance = PublicCloud(data_path=data_path)

# instance.loadCSV("kanko_all")
instance.csv_data = instance.util.loadCsv(file_name="kanko_all.csv")

instance.formatCsvToJson()
"""



