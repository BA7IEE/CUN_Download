# -*- coding:utf-8 -*-
# @FileName  :CUN.py
# @Time      :2022/5/8 下午11:08
# @Author    :tungwerl
import re

import requests
from lxml import etree

work_url = []
username = ''


def html_download(url):
    if url is None:
        return
    s = requests.Session()
    s.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    res = s.get(url)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        res = res.text
        return res
    return None


def username_get(url):
    '''
    获取用户名
    :param url: 主页链接
    :return:  用户名
    '''
    resp = etree.HTML(html_download(url))
    global username
    username = resp.xpath('//span[@class="author_name"]/text()')[0].strip()
    return username


def album_get(url):
    '''
    获取当前页面所有相册url和相册名称
    :param url: 页面url
    :return: 不返回结果，直接字典格式保存到 work_url 列表
    '''
    resp = etree.HTML(html_download(url))
    obj = resp.xpath('//div[@class="col-xs-6 col-sm-4 col-md-3 work-thumbnail"]')
    for item in obj:
        album_title = item.xpath('.//div[@class="title"]/text()')[0].strip()
        album_url = item.xpath('./a[@class="thumbnail"]/@href')[0]
        album_dict = {'album_title': album_title, 'album_url': album_url}
        work_url.append(album_dict)
        print(album_title, album_url)
    print('**********本页面的所有相册获取完毕**********')
    return


def pic_get(url, album_title):
    '''
    获取相册中图片的URL地址
    :param url: 相册URL
    :param album_title: 相册名称
    :return: 本相册所有图片URL的列表，相册名称
    '''
    resp = etree.HTML(html_download(url))
    res = resp.xpath('//div[@id="imgs_json"]/text()')[0]
    output = ''
    for i in res:
        output += str(i)
    result = re.findall(r'img":"(.*?)"', output)
    pic_url = []
    for item in result:
        pic_url.append('http://imgoss.cnu.cc/' + item)
    print('**********本相册的所有图片获取完毕**********')
    return pic_url, album_title
