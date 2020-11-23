# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 20:17
# @Author  : xzkzdx
# @File    : addons.py
import json
import os
import re
import sys
from urllib.parse import unquote
import hashlib
import json

def resource_path(relative_path):
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)


def read(fileName=""):
    if fileName != '':
        strList = fileName.split(".")
        if strList[len(strList) - 1].lower() == "json":
            with open(fileName, mode='r', encoding="utf-8") as file:
                return json.loads(file.read())


def write(filename, new_dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_dict, f, ensure_ascii=False, indent=4)
        print("写入json完成...")


import mitmproxy as mp

mykey = read(resource_path("./config.json"))


class WeiXinProxy:
    def __init__(self):
        pass

    def uin_md5(self, uin):
        if "%" in uin:
            uin = self.uin_md5(unquote(uin))
        return uin

    def request(self, flow: mp.http.HTTPFlow):
        if flow.request.host == "mp.weixin.qq.com":  #存储个人微信信息
            url_path = flow.request.path
            if url_path.startswith("/s?__biz=") and "uin=" in url_path and "key=" in url_path:
                biz = self.uin_md5(re.search(r"__biz=([^&]+)&?", url_path).group(1))
                key = re.search(r"key=([^&]+)&?", url_path).group(1)
                uin = self.uin_md5(re.search(r"uin=([^&]+)&?", url_path).group(1))
                hash_key = hashlib.md5(biz.encode("utf-8")).hexdigest()
                mykey[biz]= {"hash_key": hash_key, "biz": biz, "uin": uin, "key": key}
                write(resource_path("./config.json"),mykey)
        if flow.request.host == "m-qun.umeng100.com": # 存储umeng100信息
            url_path = flow.request.path
            cookies = flow.request.cookies # 转换cookies格式为dict
            if cookies:
                mykey['cookies']=dict(cookies)
                write(resource_path("./config.json"), mykey)  # 如果不为空保存cookies




addons = [
    WeiXinProxy()
]

if __name__ == "__main__":
    pass
