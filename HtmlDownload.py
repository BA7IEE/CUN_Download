# -*- coding:utf-8 -*-
# @FileName  :HtmlDownload.py
# @Time      :2022/5/8 下午8:49
# @Author    :tungwerl
import requests
class HtmlDownload(object):
    def donwload(self, url):
        if url is None:
            return
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        res = s.get(url)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            res = res.text
            return res
        return None