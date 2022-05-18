# -*- coding:utf-8 -*-
# @FileName  :baike.py
# @Time      :2022/5/9 下午11:05
# @Author    :tungwerl
import re

import requests


def html_download(url):
    if url is None:
        return
    s = requests.Session()
    s.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    try:
        response = s.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except requests.ConnectionError:
        return None


def newLemmaIdEnc_get(url):
    print(f'开始获取newLemmaIdEnc')
    resp = html_download(url)
    result = re.findall(r'newLemmaIdEnc:"(.*?)",', resp)
    print(f'newLemmaIdEnc值获取成功：{result}')
    return result[0]


def url_split(bk_url):
    print('开始生成URL')
    newLemmaIdEnc = newLemmaIdEnc_get(bk_url)
    url = 'https://baike.baidu.com/api/lemmapv?id=' + newLemmaIdEnc
    print(f'URL拼接成功：{url}')
    return url


url = url_split('https://baike.baidu.com/item/%E7%A6%BE%E8%91%A1%E5%85%B0/13215201?fr=aladdin')
i = 0
while i < 10000:
    html_download(url)
    i += 1
    print(f'浏览量新增：{i}')
