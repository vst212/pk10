import io
import json
import re
from urllib.request import urlopen

import requests
from PyQt5.QtGui import QImage, QPixmap
from pyquery import PyQuery as pq
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel
from pyzbar import pyzbar
from PIL import Image
import readJSON
from crawlerapi import get_history_api
from urllib.parse import unquote

from myjson import resource_path


def uin_md5(self, uin):
    if "%" in uin:
        uin = self.uin_md5(unquote(uin))
    return uin


def search(rawurl, qw, self):
    newlist = []
    try:
        biz = re.search(r"__biz=([^&]+)&?", rawurl).group(1)
        config = readJSON.read('config.json')
        config = config[biz]
        for move in range(1):
            res = get_history_api(biz=config['biz'], uin=config['uin'], key=config['key'], offset=10 * move)
            if res['errmsg'] == "ok":
                # 格式化分类列表
                dict = json.loads(res['general_msg_list'])
                for i in dict['list']:
                    newlist.append(i['app_msg_ext_info']['content_url'])
            else:
                QMessageBox.about(qw, '提示', '信息过期，请重新获取令牌！')
    except Exception as e:
        print(e)
    print(newlist)
    # 遍历一遍
    finallist = []
    try:
        for arurl in newlist:
            list = getqr(arurl)
            finallist.extend(list)
        print(finallist)
    except Exception as e:
        print(e)
    return finallist



def isqr(url):
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    img = Image.open(data_stream)
    return pyzbar.decode(img) != []


def getqr(url):
    newlist = []
    r1 = requests.get(url).text
    d = pq(r1)
    li = d('#page-content').find('img').items()
    for id in li:
        imgurl = pq(id)('img').attr('data-src')
        if imgurl and isqr(imgurl):
            newlist.append(imgurl)
        else:
            print("没有二维码")
    return newlist




