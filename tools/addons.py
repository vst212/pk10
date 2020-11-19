# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 20:17
# @Author  : xzkzdx
# @File    : addons.py
import json
import re
from urllib.parse import unquote
import hashlib

print("sd233")

import mitmproxy as mp
import redis
from .readJSON import *

mykey=read("../config.json")

class WeiXinProxy:
    def __init__(self):
        pass

    def uin_md5(self, uin):
        if "%" in uin:
            uin = self.uin_md5(unquote(uin))
        return uin

    def request(self, flow: mp.http.HTTPFlow):
        print("duquduqu")
        if flow.request.host == "mp.weixin.qq.com":
            print("开始抓取啦")
            url_path = flow.request.path
            if url_path.startswith("/s?__biz=") and "uin=" in url_path and "key=" in url_path:
                biz = self.uin_md5(re.search(r"__biz=([^&]+)&?", url_path).group(1))
                key = re.search(r"key=([^&]+)&?", url_path).group(1)
                uin = self.uin_md5(re.search(r"uin=([^&]+)&?", url_path).group(1))
                hash_key = hashlib.md5(biz.encode("utf-8")).hexdigest()
                print("抓到了：", hash_key, biz, uin, key) ##直接保持到本地txt即可 每次更新txt
                write("../config.json",{"hash_key":hash_key,"biz":biz,"uin":uin,"key":key})

addons = [
    WeiXinProxy()
]

if __name__ == "__main__":
    pass
