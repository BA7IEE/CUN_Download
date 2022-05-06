# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/5/5 下午3:08
# @Author    :tungwerl
import datetime
import os
import re
from typing import List, Union, Any

import requests
from lxml import etree


def time():
    now_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    return f'[{time_str}]'


def rd(lists):
    temp = list(set(lists))
    print(f'{time()}去重成功')
    return temp


def download_pic(url_pic, folder_name=str):
    # 指定文件的存放路径
    pic_save_path = f'/home/tungwerl/Pictures/{folder_name}/'

    # 取出URL最后一个/后的字符串并组合
    path = pic_save_path + url_pic.split('/')[-1]
    try:
        if not os.path.exists(pic_save_path):
            os.makedirs(pic_save_path)
        if not os.path.exists(path):
            r = requests.get(url_pic)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print(f"{time()}图片{url_pic.split('/')[-1]}保存成功")
        else:
            print(f"{time()}图片{url_pic.split('/')[-1]}已存在，跳过")
    except:
        print(f"{time()}图片{url_pic}获取失败")


def html_obtain(url):
    """
    Get请求获取HTML
    :param url:url
    :return: HTML
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(f'{time()}[{url}]解析成功')
        return resp.text
    else:
        print(f'{time()}html获取失败，状态码：{resp.status_code}')


def url_page_obtain(url):
    resp = etree.HTML(html_obtain(url))
    page_url = resp.xpath('//ul[@class="pagination"]/li/a/@href')
    page_url.append(url)
    print(f'{time()}成功获取{len(page_url)}个页面')
    return rd(page_url)


def url_album_obtain(page_url: object) -> object:
    resp = etree.HTML(html_obtain(page_url))
    url_album = resp.xpath('//a[@class="thumbnail"]/@href')
    return url_album


def url_pic_obtain(album_url):
    resp = etree.HTML(html_obtain(album_url))
    res = resp.xpath('//div[@id="imgs_json"]/text()')[0]
    users_name = resp.xpath('//span[@class="author-info"]/a/strong/text()')[0].strip()
    work_title = resp.xpath('//h2[@class="work-title"]/text()')[0].strip()
    output = ''
    for i in res:
        output += str(i)
    result = re.findall(r'img":"(.*?)"', output)
    urls_pic: List[Union[str, Any]] = []
    print(f'{time()}正在获取相册《{work_title}》的图片URL')
    for i in result:
        urls_pic.append('http://imgoss.cnu.cc/' + i)
    save_path = users_name + '/' + work_title
    print(f'{time()}相册《{work_title}》{len(urls_pic)}张图片URL获取完毕')
    return urls_pic, save_path


def all_albums(url_users):
    all_album = []
    for page in url_page_obtain(url_users):
        for album in url_album_obtain(page):
            all_album.append(album)
    print(f'{time()}该用户所有相册获取成功，共计{len(all_album)}个相册')
    return all_album


def main():
    url = input('请输入需要下载用户的主页URL:')
    for i in all_albums(url):
        pic_url, save_path = url_pic_obtain(i)
        print(f'{time()}《{save_path}》所有图片获取完毕，准备开始下载......')
        for it in pic_url:
            download_pic(it, save_path)
        print(f'{time()}相册《{save_path}》所有图片下载完成')
    print(f'{time()}所有图片下载完成，程序退出')


if __name__ == '__main__':
    main()
