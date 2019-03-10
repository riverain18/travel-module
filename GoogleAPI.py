#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import requests
import urllib
import json
import time

sys.path.append(os.path.dirname(__file__))
from Config import *

class GoogleAPI:

    def __init__(self, key, load_data_path, write_data_path):
        self.key = key
        self.load_data_path = load_data_path
        self.write_data_path = write_data_path

        self.place_search_data = {}
        self.place_detail_data = {}


    def writeJson(self, file_name, json_data):
        '''
        jsonデータをjsonファイルに書き込む関数
        '''
        fw = open("{0}/{1}.json".format(self.write_data_path, file_name), "w")
        json.dump(json_data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


    def getPlaceSearch(self, name):
        '''
        Place Search APIを使用する関数
        input : name
        output : json_data (place_id etc.)
        '''

        # 待ち時間
        time.sleep(1.0)

        # HTTP Request の URL を設定
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

        # Parameters を設定
        params = {}
        params["key"] = self.key
        params["input"] = name
        params["inputtype"] = "textquery"
        params["language"] = "ja"
        params["fields"] = "name,id,place_id"

        # urllibを使用する場合
        # p = url + "?" + urllib.parse.urlencode(params)
        # res = urllib.request.urlopen(p)
        # print(res.read().decode("utf-8"))

        # requestsを使用する場合
        json_data = requests.get(url, params).json()

        # Status Codeでエラーチェック
        if json_data["status"] == "OK":

            # candidatesの中身だけ抽出
            json_data = json_data["candidates"][0]

            # 大元のjsonに登録
            self.place_search_data[name] = json_data

            return True

        else:
            return False


    def getPlaceDetail(self, name, name_pc, place_id, key_num):
        '''
        Google Places APIを用いて、
        場所(place_id)の詳細を取得する関数
        input : place_id
        output : json_data
        '''

        # 待ち時間
        time.sleep(1.0)

        # HTTP Request の URL を設定
        url = "https://maps.googleapis.com/maps/api/place/details/json"

        # Parameters を設定
        params = {}
        params["key"] = self.key
        params["placeid"] = place_id
        params["language"] = "ja"
        params["fields"] = "formatted_address,formatted_phone_number,geometry,international_phone_number,name,opening_hours,photos,place_id,price_level,rating,reviews,url,website"

        # requestsを使用する場合
        json_data = requests.get(url, params).json()

        # Status Codeでエラーチェック
        if json_data["status"] == "OK":

            # Resultの中身だけ抽出
            json_data = json_data["result"]

            # 公共クラウドシステムの名前を追加
            json_data["name_pc"] = name_pc

            # 大元のjsonに登録
            self.place_detail_data[key_num] = json_data

            return True

        else:
            return False
        





key = ""
data_path = os.path.dirname(os.path.abspath(__file__)) + "/../data"
config = Config()
instance = GoogleAPI(key, load_data_path=config.LOAD_DATA_PATH, write_data_path=config.WRITE_DATA_PATH)
# instance.getPlaceSearch("岐阜城")
# instance.getPlaceSearch("名古屋城")
# instance.writeJson("place_search_sample", instance.place_search_data)

instance.getPlaceDetail("熊本城", "熊本城", "ChIJqw4uj3mpA2ARSslCVWXDcSg", 0)
instance.writeJson("place_detail_sample2", instance.place_detail_data)








