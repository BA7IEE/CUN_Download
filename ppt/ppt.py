# -*- coding:utf-8 -*-
# @FileName  :ppt.py
# @Time      :2022/5/18 下午7:36
# @Author    :tungwerl
import datetime
import re

import requests
from lxml import etree
from sql import DB_OP

db = '/mnt/hgfs/ShareFile/ppt.db'
url = 'https://www.1ppt.com/data/sitemap.html'

def log_time():
    now_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    return f'[{time_str}] '

def html_download(url):
    print(f'{log_time()}开始下载HTML')
    if url is None:
        return
    s = requests.Session()
    s.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    try:
        response = s.get(url)
        if response.status_code == 200:
            response.encoding = 'gb2312'
            print(f'{log_time()}HTML下载成功（{url}）')
            return response.text
    except requests.ConnectionError:
        return None

def class_one_get(url):
    print(f'{log_time()}开始获取')
    resp = etree.HTML(html_download(url))
    resp = resp.xpath('//div[@class="linkbox"]')[0:-7]
    coon = DB_OP(db)
    for i in resp:
        class_one_name = i.xpath('./h3/a/text()')[0]
        class_one_url = 'https://www.1ppt.com' + i.xpath('./h3/a/@href')[0]
        sql = f"insert into class_one ( name, url ) values ('{class_one_name}', '{class_one_url}')"
        coon.addRecord('class_one', 'url', class_one_url, sql)
    coon.db_close()

def pages_num_get(url):
    """
    获取类目的总页数并返回
    :param url: 类目的url
    :return: 总页数
    """
    resp = etree.HTML(html_download(url))
    resp = resp.xpath('//ul[@class="pages"]/li/a/@href')[-1]
    pages_num = re.findall(r"\d+", resp)[0]
    print(f'{log_time()}总页数获取成功，一共{pages_num}页')
    return pages_num

def url_generate(name, url):
    num = int(pages_num_get(url))
    coon = DB_OP(db)
    for i in range(1, num + 1):
        pages_url = (f'{url}ppt_{url.split("/")[-2]}_{i}.html')
        print(pages_url)
        sql = f"insert into pages_url ( name, url ) values ('{name}', '{pages_url}')"
        coon.addRecord('pages_url', 'url', pages_url, sql)
    coon.db_close()

def all_url_generate():
    """
    通过数据库中class_one表中，所有类目url生成所有页面的url
    :return:
    """
    while True:
        coon = DB_OP(db)
        if coon.getRecord('class_one') is not None:
            value = coon.getRecord('class_one')
            name, url = value[1], value[2]
            coon.db_close()
            url_generate(name, url)
            coon = DB_OP(db)
            coon.delRecord('class_one','url',url)
        else:
            print('url为空，所有url处理完毕')
            coon.db_close()
            break

def ppt_url_get(url):
    """
    获取单个页面的20个ppt详情，url和下载数量、封面
    :param url: 页面的url
    :return:
    """
    print(f'{log_time()}开始获取')
    resp = etree.HTML(html_download(url))
    resp = resp.xpath('//ul[@class="tplist"]/li')
    coon = DB_OP(db)
    for i in resp:
        class_name = i.xpath('./span/a/text()')[0]
        name = i.xpath('./h2/a/text()')[0]
        download_nums = i.xpath('./span/text()')[1][1:-1]
        ppt_url = f"https://www.1ppt.com{i.xpath('./h2/a/@href')[0]}"
        img_url = i.xpath('./a/img/@src')[0]
        sql = f"""insert into ppt ( class_name, name, download_nums, ppt_url, img_url ) values ("{class_name}","{name}", "{download_nums}", "{ppt_url}", "{img_url}")"""
        print(sql)
        coon.addRecord('ppt', 'ppt_url', ppt_url, sql)
    coon.db_close()

def all_ppt_url_get():
    """
    获取所有的ppt详情页url和下载数量、封面
    :return:
    """
    while True:
        coon = DB_OP(db)
        if coon.getRecord('pages_url') is not None:
            url = coon.getRecord('pages_url')[2]
            ppt_url_get(url)
            coon = DB_OP(db)
            coon.delRecord('pages_url', 'url', url)
        else:
            print('url为空，所有url处理完毕')
            coon.db_close()
            break

def download_url():
    pass


# 获取大类目url
# class_one_get(url)
# 生成所有页面url
# all_url_generate()
# 获取所有ppt详情页url
all_ppt_url_get()