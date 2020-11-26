import json
import re
import time

import requests
from pyquery import PyQuery as pq
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel
from requests_toolbelt.utils import dump

import readJSON



def getqrimglist(rawurl, qw):
    newlist = []
    localdata = readJSON.read('data.json')
    try:
        source = re.search(r"source=([^&]+)&?", rawurl).group(1)
        menulist = getmenu(rawurl)

        for id in menulist:
            res = getimgapi(id, source)
            if not res['msg']:
                imgurl = res['data']  ##添加到data.json 列表
                newlist.append(imgurl)
            else:
                QMessageBox.about(qw, '提示', '账号频繁，请切换账号获取')
                break
    except Exception as e:
        print(e)
    localdata[rawurl] = {"title":localdata[rawurl]['title'],"pic":newlist+localdata[rawurl]['pic']}
    readJSON.write('data.json', localdata)  # 写入到缓存
    return newlist


def getmenu(url):
    newlist = []
    r1 = requests.get(url).text
    d = pq(r1)
    li = d('#menuList').find('p').items()
    for id in li:
        imgurl = pq(id)('p').attr('categoryid')
        print(imgurl)
        newlist.append(imgurl)
    return newlist


def getimgapi(id, sourceid):
    config = readJSON.read('config.json')
    cookies = config['cookies']
    headers = {
        'Cookie': 'robot_center_mobile_login_cookie="%s"' % (cookies['robot_center_mobile_login_cookie']),
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
    }
    # s.cookies = cookie
    data = {"id": id, "source": sourceid}
    uri_api = "https://m-qun.umeng100.com/indistandalong/m/getQrcode.ajax"
    resp_json = requests.post(uri_api, data=json.dumps(data), headers=headers).json()
    print(resp_json)
    return resp_json
