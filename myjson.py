import json
import os
import sys


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


def resource_path(relative_path):
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)