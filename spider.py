#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created by LiuLei on 2017/10/27.
"""
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import json
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
    爬取笔趣阁小说网站
"""

class Spider(object):

    article_title_dict = {}
    page_url_list = []

    def __init__(self, baseUrl, article_index):
        self.BaseUrl = baseUrl
        self.page_url_list = self.get_page_list(article_index)

    def get_page_list(self, article_index):
        """
        获取文章目录列表
        :param article_index: 文章的index ID
        :return:
        """
        article_url = "%s/%s/" % (self.BaseUrl, article_index)
        page_content = self.get_request_for_url(article_url)
        soup = BeautifulSoup(page_content)
        dd_a_doc = soup.select("dd > a")
        for a_doc in dd_a_doc:
            article_page_url = a_doc['href']
            article_title = a_doc.get_text()
            if article_page_url:
                self.article_title_dict[article_page_url] = article_title
        title_url_list = self.article_title_dict.keys()
        title_url_list.sort()
        return title_url_list

    def get_page_detial(self):
        """
        获取页面的详情信息
        :return:
        """
        for page in self.page_url_list:
            # if page != '/43_43074/2383292.html':
            #     continue
            page_url = '%s%s' % (self.BaseUrl, page)
            title_name = self.article_title_dict.get(page)
            print '正在爬取 %s 的内容' % title_name
            page_content = self.get_request_for_url(page_url)
            page_soup = BeautifulSoup(page_content)
            content_doc = page_soup.find("div", id="content")
            content_text = content_doc.get_text()
            content_text = content_text.replace('readx();﻿', '')
            content_text = content_text.replace('    ', "\r\n")
            content = "%s\n%s\n\n" % (title_name, content_text)
            self.write_to_file(content.decode('utf-8'), 'text.txt')


    def get_request_for_url(self, url):
        """
        获取指定url的request请求
        :param url:
        :return:
        """
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()

    def write_to_file(self, content, filename):
        with(open(filename, 'a')) as f:
            f.write(content)

spider = Spider("http://www.biqudu.com", "43_43074/")
spider.get_page_detial()
