# -*- coding:utf-8 -*-
# @FileName  :SpiderMan.py
# @Time      :2022/5/8 下午8:54
# @Author    :tungwerl

from HtmlDownload import HtmlDownload
from UrlManage import UrlManager

class SpinderMan(object):
    def __init__(self):
        self.manager = UrlManager
        self.downloader = HtmlDownload
    def crawl(self, root_url):
        self.manager.add_new_url(root_url)
