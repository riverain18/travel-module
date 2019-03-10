#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import time
import urllib
import urllib3
import requests
from bs4 import BeautifulSoup
import re
import copy

sys.path.append(os.path.dirname(__file__))
from util.Util import *
from BrowserController import *
from Scraping import *


class AppleStore:

    def __init__(self, bcon, scrap, util):
        self.bcon = bcon
        self.scrap = scrap
        self.util = util
        self.url = None
        self.company_code = None
        self.app_id = None
        self.json_data = None
        self.json_data_all = None


    def setUrl(self, company_code="jp", app_id="382775642"):
        '''
        対象アプリのReview URLを設定する関数
        '''
        if self.url is None:
            self.url = "https://itunes.apple.com/{0}/rss/customerreviews/id={1}/sortBy=mostRecent/xml".format(company_code, app_id)
            self.company_code = company_code
            self.app_id = app_id


    def getReviewsXml(self, company_code="jp", app_id="382775642"):
        '''
        Reviewのデータを取得する関数
        '''
        if self.url is None:
            self.setUrl(company_code=company_code, app_id=app_id)

        if self.json_data_all is None:

            self.json_data_all = {"result":[]}

            while True:
                # XML形式でデータを取得
                self.scrap.parseHtml(self.url)
                
                entries = self.scrap.soup.find_all("entry")
                
                for entry in entries:
                    json_data = {}
                    date = entry.find("updated")
                    title = entry.find("title")
                    review = entry.find("content")
                    author = entry.find("author").find("name")
                    rating = entry.find("im:rating")
                    json_data["date"] = date.text
                    json_data["title"] = title.text
                    json_data["review"] = review.text
                    json_data["author"] = author.text
                    json_data["rating"] = int(rating.text)
                    self.json_data_all["result"].append(json_data)

                last_url = self.scrap.soup.find("link", rel="last").attrs["href"]
                next_url = self.scrap.soup.find("link", rel="next").attrs["href"]
                self.url = next_url
                print(next_url)

                if next_url == last_url:
                    break
                time.sleep(3.0)
        return self.json_data_all



    def getReviews(self, company_code="jp", app_id="382775642"):
        '''
        Reviewのデータを取得する関数
        '''
        if self.url is None:
            self.setUrl(company_code=company_code, app_id=app_id)

        json_data_all = {"result":[]}
        json_data = {}
        if self.json_data is None:

            while True:
                # Json形式でデータを取得
                json_data = {}
                response = urllib.request.urlopen(self.url)
                json_data = json.loads(response.read().decode("utf-8"))

                # 必要なデータを抽出して、リストに追加
                for entry in json_data["feed"]["entry"]:
                    content = {}
                    content["author"] = entry["author"]["name"]["label"]
                    content["review"] = entry["content"]["label"]
                    content["rating"] = entry["im:rating"]["label"]
                    content["title"] = entry["title"]["label"]
                    json_data_all["result"].append(content)

                # 次のレビューのURLが存在するかどうか
                next_url = ""
                for attribute in json_data["feed"]["link"]:
                    if attribute["attributes"]["rel"] == "next":
                        next_url = attribute["attributes"]["href"]
                        self.url = next_url
                        print(next_url)

                if next_url == "":
                    break
                time.sleep(3.0)

        return json_data_all


    def scrapReviews(self, file_name, company_code="jp", app_id="382775642"):
        '''
        Reviewをスクレイピングする関数
        '''
        self.util.writeJson(json_data=self.getReviewsXml(company_code=company_code, app_id=app_id), file_name=file_name)




class GooglePlay:

    def __init__(self, bcon, scrap, util):
        self.bcon = bcon
        self.scrap = scrap
        self.util = util
        self.url = None
        self.company_code = None
        self.app_id = None
        self.json_data = None
        self.json_data_all = None

    def setUrl(self, app_id):
        '''
        対象アプリのReview URLを設定する関数
        '''
        if self.url is None:
            self.url = "https://play.google.com/store/apps/details?id={0}&showAllReviews=true".format(app_id)
            self.app_id = app_id

    def getReviewsBrowser(self, app_id):
        '''
        Reviewのデータを取得する関数
        '''
        if self.url is None:
            self.setUrl(app_id=app_id)

        if self.json_data_all is None:
            self.json_data_all = {"result":[]}

            # Browserを起動
            self.bcon.openBrowser()
            self.bcon.openWebPage(self.url)

            # ページ情報を取得
            self.bcon.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            text = self.bcon.driver.page_source

            # 最下層までスクロール
            while True:
                self.bcon.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3.0)
                text_scroll=self.bcon.driver.page_source
                if text != text_scroll:
                    text = text_scroll
                else:
                    break

            # ページ情報を解析
            soup = BeautifulSoup(text, "lxml")

            # Review情報を抽出
            review_list = soup.find_all("span", jsname="bN97Pc")
            date_list = soup.find_all("span", class_="p2TkOb")
            author_list = soup.find_all("span", class_="X43Kjb")
            rating_list = soup.find_all("div", role="img")
            
            # rating整形
            rating_list_copy = copy.copy(rating_list)
            rating_list_copy = rating_list[1:len(review_list)+1] # Top(総合?)と他アプリを除く
            rating_list = copy.copy(rating_list_copy)

            # Jsonデータとして保存
            for review, date, author, rating in zip(review_list, date_list, author_list, rating_list):
                json_data = {}
                json_data["review"] = review.text
                json_data["date"] = date.text
                json_data["author"] = author.text
                json_data["rating"] = rating.attrs["aria-label"]
                self.json_data_all["result"].append(json_data)

        # Browserを閉じる
        self.bcon.closeBrowser()

        return self.json_data_all


    def scrapReviews(self, file_name, app_id):
        '''
        Reviewをスクレイピングする関数
        '''
        self.util.writeJson(json_data=self.getReviewsBrowser(app_id=app_id), file_name=file_name)



config = Config()
# app_store = AppleStore(BrowserController(), Scraping(), Util(load_data_path=config.LOAD_DATA_PATH, write_data_path=config.WRITE_DATA_PATH))
# app_store.scrapReviews(file_name="test.json", company_code="jp", app_id="382775642")

googleplay = GooglePlay(BrowserController(), Scraping(), Util(load_data_path=config.LOAD_DATA_PATH, write_data_path=config.WRITE_DATA_PATH))
googleplay.scrapReviews(file_name="test2.json", app_id="com.brother.mfc.brprint")