# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/5/2 下午11:59
# @Author    :tungwerl
import os
import re
import requests
from lxml import etree


def page_urls():
    """
    获取所有页面的URL
    :return: list(所有页面的URL)
    """
    url = 'http://www.cnu.cc/users/545834'
    hd = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    res = requests.get(url, headers=hd)
    res = etree.HTML(res.text)
    print('正在获取页面url')
    page_url = res.xpath('//ul[@class="pagination"]/li/a/@href')
    page_url.append(url)
    print(page_url)
    print('页面获取获取完毕')
    print('*' * 50)
    return page_url


def Download_pic(pic_url):
    # 指定文件的存放路径
    pic_save_path = '/home/tungwerl/Pictures/test/'

    # 取出URL最后一个/后的字符串并组合
    path = pic_save_path + pic_url.split('/')[-1]
    try:
        if not os.path.exists(pic_save_path):
            os.mkdir(pic_save_path)
        if not os.path.exists(path):
            r = requests.get(pic_url)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片保存成功")
        else:
            print("图片已存在，跳过")
    except:
        print("图片获取失败")


def img_url(album_url):
    hd = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    res = requests.get(album_url, headers=hd)
    res = etree.HTML(res.text)
    page_url = res.xpath('//div[@id="imgs_json"]/text()')[0]
    output = ''
    for i in page_url:
        output += str(i)
    result = re.findall(r'img":"(.*?)"', output)
    img_url = []
    print('正在获取图片url')
    for i in result:
        img_url.append('http://imgoss.cnu.cc/' + i)
        print(i)
    print('当前页面图片获取完毕')
    print('*' * 50)
    return img_url


def albums(page_url):
    """
    获取每个页面下所有相册的url
    :param page_url: 传入页面url
    :return: 返回list(相册url)
    """
    hd = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
    res = requests.get(page_url, headers=hd)
    res = etree.HTML(res.text)
    page_url = res.xpath('//a[@class="thumbnail"]/@href')
    album = []
    for i in page_url:
        album.append(i)
    print(album)
    print('正在获取相册URL')
    print('相册URL获取完毕')
    print('*' * 50)
    return album


for page_urls in page_urls():
    for album in albums(page_urls):
        for img in img_url(album):
            Download_pic(img)
