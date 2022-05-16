# -*- coding:utf-8 -*-
# @FileName  :zhidao.py
# @Time      :2022/5/15 下午2:02
# @Author    :tungwerl
import random
import requests
import js2py


def ip_random():
    url = "http://127.0.0.1:16888/random?protocol=http"
    response = requests.request("GET", url)
    return response.text


def js_utdata():
    js = open("./utdata.js", 'r', encoding='utf-8').read()
    context = js2py.EvalJs()
    context.execute(js)
    return context.getutdata()


def getRadon(randomlength):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def zd_post(qid, aid, proxies):
    url = "http://zhidao.baidu.com/submit/ajax/"
    payload = f"cm=100669&qid={qid}&aid={aid}&type=1&utdata={js_utdata()}"
    headers = {
        'Content-Type': 'text/plain',
        'Cookie': f'BAIDUID={getRadon(32)}:FG=1; ZD_ENTRY=empty'
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    if response.json()['errorNo'] == '0':
        print(f'proxies {proxies["http"][7:-5]} 点赞成功')
    else:
        print(f'点赞失败 {response.json()}')


i = 0
while i < 5:
    proxies = {
        "http": ip_random(),
    }
    print(proxies)
    qid = '590232883198347925'
    aid = '3352330972'
    zd_post(qid, aid, proxies)
    zd_post(qid, aid, proxies)
