# -*- coding:utf-8 -*-
# @FileName  :CUN_class.py
# @Time      :2022/5/13 下午6:13
# @Author    :tungwerl
import datetime
import os
import re

import requests
from lxml import etree


def log_time():
    now_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    return f'[{time_str}] '
def info_print():
    print('请选择功能--------------')
    print('1、下载该用户所有图片')
    print('2、下载指定相册的图片')
    print('3、退出系统')
    print('-' * 20)


class Download_CUN:
    work_url = set()
    page_url = set()
    username = ''

    def html_download(self, url):
        print(f'{log_time()}开始下载HTML')
        if url is None:
            return
        s = requests.Session()
        s.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        try:
            response = s.get(url)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                print(f'{log_time()}HTML下载成功（{url}）')
                return response.text
        except requests.ConnectionError:
            return None

    def username_get(self, url):
        '''
        获取用户名
        :param url: 主页链接
        :return:  用户名
        '''
        print(f'{log_time()}开始获取用户名')
        resp = etree.HTML(self.html_download(url))
        self.username = resp.xpath('//span[@class="author_name"]/text()')[0].strip()
        print(f'{log_time()}用户名获取成功：{self.username}')
        return self.username

    def page_get(self, url):
        '''
        获取页面URL
        :param url: 主页url
        :return:
        '''
        print(f'{log_time()}开始解析所有页面')
        resp = etree.HTML(self.html_download(url))
        pages = resp.xpath('//ul[@class="pagination"]/li/a/@href')
        self.page_url.add(url)
        for i in pages:
            self.page_url.add(i)
            print(f'{log_time()}{i}')
        print(f'{log_time()}页面解析完成，共{len(self.page_url)}页')
        for item in self.page_url:
            print(f'{log_time()}{item}')

    def album_get(self, url):
        '''
        获取当前页面所有相册url
        :param url: 页面url
        :return: 不返回结果，直接字典格式保存到 work_url 列表
        '''
        print(f'{log_time()}开始解析相册链接')
        resp = etree.HTML(self.html_download(url))
        album_url = resp.xpath('//a[@class="thumbnail"]/@href')
        print(f'{log_time()}当前页面相册解析完成')
        for i in album_url:
            self.work_url.add(i)
            print(f'{log_time()}{i}')

    def pic_get(self, url):
        '''
        获取相册中图片的URL地址
        :param url: 相册URL
        :return: 本相册所有图片URL的列表，相册名称
        '''
        print(f'{log_time()}开始解析图片链接和相册名称')
        resp = etree.HTML(self.html_download(url))
        res = resp.xpath('//div[@id="imgs_json"]/text()')
        title = resp.xpath('//h2[@class="work-title"]/text()')[0].strip()
        output = ''
        for i in res[0]:
            output += str(i)
        result = re.findall(r'img":"(.*?)"', output)
        pic_url = []
        for item in result:
            pic_url.append('http://imgoss.cnu.cc/' + item)
        print(f'{log_time()}相册《{title}》解析完成，共{len(pic_url)}张')
        return pic_url, title

    def download_pic(self, pic_url, pic_save_path):
        # 取出URL最后一个/后的字符串并组合
        path = pic_save_path + pic_url.split('/')[-1]
        try:
            if not os.path.exists(pic_save_path):
                os.makedirs(pic_save_path)
            if not os.path.exists(path):
                r = requests.get(pic_url)
                r.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(r.content)
                    print(f"{log_time()}{pic_url.split('/')[-1]}下载成功")
            else:
                print(f"{log_time()}{pic_url.split('/')[-1]}已存在，跳过")
        except:
            print(f"{log_time()}{pic_url}获取失败")

    def album_pic_download(self, url):
        url, path = self.pic_get(url)
        path = f'/home/tungwerl/Pictures/{path}/'
        for i in url:
            self.download_pic(i, path)

    def all_pic_download(self, url):
        self.username_get(url)
        self.page_get(url)
        for page in self.page_url:
            self.album_get(page)
        print(f'{log_time()}所有相册解析完成，共{len(self.work_url)}个')
        for pic in self.work_url:
            pic_url, path = self.pic_get(pic)
            save_path = f'/home/tungwerl/Pictures/{self.username}/{path}/'
            print(f'{log_time()}开始下载图片')
            for i in pic_url:
                self.download_pic(i, save_path)
            print(f'{log_time()}当前相册《{path}》下载完成,共{len(pic_url)}张')

cun = Download_CUN()
while True:
    # 1. 显示功能界面
    info_print()

    # 2. 用户输入功能序号
    user_num = int(input('请输入功能序号：'))

    # 3. 按照用户输入的功能序号，执行不同的功能(函数)
    # 如果用户输入1，执行添加；如果用户输入2，执行删除... -- 多重判断
    if user_num == 1:
        # print('添加')
        while True:
            url = input('请输入用户主页地址：')
            if 'users' in url:
                cun.all_pic_download(url)
                print(f'{log_time()}**********下载完成**********')
                break
            else:
                print('链接错误，请输入主页链接')
            continue

    elif user_num == 2:
        # print('删除')
        while True:
            url = input('请输入相册地址：')
            if 'works' in url:
                cun.album_pic_download(url)
                print(f'{log_time()}**********下载完成**********')
                break
            else:
                print('链接错误，请输入相册链接')
            continue
    elif user_num == 3:
        # print('退出系统')
        # 程序要想结束，退出终止while True -- break
        exit_flag = input('确定要退出吗？yes or no：')
        if exit_flag == 'yes':
            break
    else:
        print('输入的功能序号有误')

