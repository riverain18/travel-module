#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

sys.path.append(os.path.dirname(__file__))
from Scraping import *
from util.Util import *
from Config import *


class BrowserController:

    def __init__(self):
        # Option
        self.options = webdriver.chrome.options.Options()

        # OptionのHeadless Browser指定
        # Comment OutでBrowserを表示
        #self.options.add_argument("-headless")

        # Driver Path
        self.driver_path = "https://www.google.co.jp/"

        # Driver
        self.driver = None

        # TitleとURLの結果を保存するリスト
        self.title_list = []
        self.url_list = []

        # Scraping
        self.scraping = Scraping()

        # Config
        self.config = Config()

        # Util
        self.util = Util(load_data_path=self.config.LOAD_DATA_PATH, write_data_path=self.config.WEB_DATA_PATH)


    def openBrowser(self):
        '''
        Browserを開く関数
        '''
        self.driver = webdriver.Chrome(chrome_options=self.options)


    def openWebPage(self, url):
        '''
        WebPageを開く関数
        '''
        self.driver.get(url)


    def searchKeyWord(self, keyword):
        '''
        KeyWordで検索を行う関数
        '''

        # 検索窓を取得
        input_elem = self.driver.find_element_by_name("q")

        # KeyWordを入力
        input_elem.send_keys(keyword)

        # 待ち時間
        time.sleep(1.0)

        # 検索を開始
        input_elem.send_keys(Keys.RETURN)

        # 待ち時間
        time.sleep(1.0)


    def getSearchResults(self, data_path, num):
        '''
        検索結果を取得する関数
        '''

        time.sleep(3.0)
        length = len(self.driver.find_elements_by_class_name("g"))
        print(length)
        time.sleep(2.0)

        # 検索結果でfor loop
        for i, g in enumerate(self.driver.find_elements_by_class_name("g")):

            time.sleep(3.0)

            # 10件以降はスルー
            if i >= 10:
                continue

            # 「こちらを検索しますか」の対処
            if i == length-1 and "こちらを検索しますか" in g.text:
                continue

            # Google Map の結果の対処
            if i == length-1:
                continue

            try:

                # TitleとURLを取得
                title = g.find_element_by_tag_name("h3").text
                url = g.find_element_by_tag_name("a").get_attribute("href")

                # TitleとURLの結果を保存
                self.title_list.append(title)
                self.url_list.append(url)

                print(title)
                print(url)

                # Scraping実行
                self.scraping.parseHtml(url)
                text = self.scraping.getText()

                # Scraping結果を保存
                self.util.writeTextFree(data_path=data_path, text_data=text, file_name="rank_{0:02d}.txt".format(i+1))

            except:
                print("###### Error ! ######")

            # 待ち時間
            time.sleep(3.0)

        # title と url の情報を Jsonファイルで保存
        json_data = {}
        for i, (title, url) in enumerate(zip(self.title_list, self.url_list)):
            json_data["{0:02d}".format(i+1)] = {"title": title, "url": url}
        self.util.writeJsonFree(data_path=self.config.WEB_DATA_PATH+"/title_url", json_data=json_data, file_name="{0:05d}_title_url.json".format(num))
        self.title_list = []
        self.url_list = []


    def closeBrowser(self):
        '''
        全てのBrowserを閉じる関数
        '''
        self.driver.quit()


if __name__ == '__main__':

    """
    test_path = None
    instance = BrowserController()
    instance.openBrowser()
    instance.openWebPage("https://www.google.co.jp/")
    instance.searchKeyWord("テスト", test_path)
    instance.getSearchResults()
    """
