# -*- coding: utf-8 -*-
# @Author: Admin
# @Date:   2019-11-01 16:52:34
# @Last Modified by:   Admin
# @Last Modified time: 2019-11-01 18:18:14
import json

def read(fileName=""):
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())


def write(filename,new_dict):
    with open(filename,"w",encoding="utf-8") as f:
       json.dump(new_dict,f,ensure_ascii=False,indent = 4)
       print("写入json完成...")