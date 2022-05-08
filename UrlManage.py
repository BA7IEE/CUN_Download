# -*- coding:utf-8 -*-
# @FileName  :UrlManage.py
# @Time      :2022/5/8 下午8:32
# @Author    :tungwerl
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        """
        判断是否有未爬取的url
        :return:
        """
        return self.new_url_size() != 0

    def get_new_url(self):
        """
        获取一个未爬取的URL，并在爬取之后添加到已爬取的集合中
        :return:
        """
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        """
        将新的链接添加到未爬取的集合中（单个链接）
        :param url:
        :return:
        """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """
        将新的链接添加到未爬取的集合中（集合）
        :param urls:
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_uel(url)

    def new_url_size(self):
        """
        获取未爬取URL的数量
        :return:
        """
        return len(self.new_urls)

    def old_url_size(self):
        """
        获取已爬取的URL数量
        :return:
        """
        return len(self.old_urls)