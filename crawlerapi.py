# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/6/21 11:14
# @File   : crawlerapi.py
import re
from json import loads
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
import html
import time

import requests

from settings import USER_AGENT, USER_AGENT_WECHAT





def get_html_api(article_url: str, use_key: bool = False, **kwargs):
    """
    :param article_url: 带参数的历史文章链接
    :param use_key: 是否使用key
    :param kwargs: key && uin
    :return:
    """
    if use_key:
        article_url = article_url + '&key={key}&ascene=1&uin={uin}'.format(**kwargs)
    request = Request(article_url, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    return html.unescape(req_resp.read().decode())


def get_platform_info_from_url(info_uri: str):
    request = Request(info_uri, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    html_content = html.unescape(req_resp.read().decode())
    meta_values = re.findall(r"<span class=\"profile_meta_value\">(.*?)</span>", html_content)
    wx_id_unique = re.search(r"user_name = \"([\w-]+)\";", html_content).group(1)
    wx_bizs = re.search(r"var biz = \"([\w=]*)\"\|\|\"([\w=]*)\";", html_content).groups()
    return {
        "account_name": re.search(r"nickname = \"([\w-]+)\"", html_content).group(1),
        "account_id": meta_values[0] if meta_values[0] else wx_id_unique,
        "account_biz": wx_bizs[0] if wx_bizs[0] else wx_bizs[1],
        "account_id_unique": wx_id_unique,
        "account_logo": re.search(r"head_?img = \"(https?:\/\/wx.qlogo.cn/mmhead/[\w\/]+)\"", html_content).group(1),
        "account_desc": meta_values[1],
        "account_url": info_uri,
        "created": f"{int(time.time())}",
    }


def get_article_comment_id_api(article_url: str):
    request = Request(article_url, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    html_content = req_resp.read().decode()
    try:
        _comment_id = re.search(r"comment_id = \"(\d*)\"", html_content).group(1)
    except AttributeError as e:
        print(e.args)
        raise e
    return _comment_id



def get_history_api(**kwargs):
    """
    获取公众号历史文章的 api 接口
    :param biz: 公众号的识别码
    :param uin: 登陆的微信账号的识别码
    :param key: 获取历史信息必要的 key
    :param offset: 偏移量
    :param count: 历史图文发布的次数，一次是多图文，最大值10，即获取偏移量后最近10次发布的所有图文消息
    :return: 解析好的json格式字典
    """

    def match_item_info(item_dict, article_publish_time):
        """
        文章详情获取
        :param item_dict: 包含单个文章信息的字典
        :return: 结构化的文章信息
        """
        article_title = item_dict.get('title', '')
        article_author = item_dict.get("author", "")
        article_digest = item_dict.get("digest", "")
        article_content_url = item_dict.get("content_url", "").replace("&amp;", "&")
        article_cover_url = item_dict.get("cover", "").replace("&amp;", "&")
        article_source_url = item_dict.get("source_url", "").replace("&amp;", "&")
        copyright_stat = item_dict.get("copyright_stat", 0)
        copy_right = 1 if copyright_stat == 11 else 0
        return {
            "article_title": article_title,  # 文章标题
            "article_author": article_author,  # 文章作者
            "article_publish_time": article_publish_time,  # 文章发布时间
            "article_digest": article_digest,  # 文章摘要
            "article_content_url": article_content_url,  # 文章详情链接
            "article_cover_url": article_cover_url,  # 封面图片链接
            "article_source_url": article_source_url,  # 源文链接
            "article_copy_right": copy_right,  # 原创
        }

    uri_api = "http://mp.weixin.qq.com/mp/profile_ext"
    form_data = {
        "action": "getmsg",
        "__biz": kwargs["biz"],
        "offset": kwargs["offset"],
        "count": kwargs.get("count", 10),
        "uin": kwargs["uin"],
        "key": kwargs["key"],
        "f": "json",
    }
    uri_api=uri_api+"?action=getmsg&__biz=%s&uin=%s&key=%s&f=json&offset=%s&count=10&pass_ticket=82dn7Dv7AFbOrM7SkzKQhr91VKDD0H7sV5v1Mada3aNsnsxRCh9bnzLSvfKxpDTZ"%(kwargs["biz"],kwargs["uin"],kwargs["key"],0)
    resp_json=requests.get(uri_api).json()
    return resp_json






def split_article_url2mis(article_url: str):
    # print(article_url)
    return {
        "mid": re.search(r"mid=(\d+)&?", article_url).group(1),
        "sn": re.search(r"sn=(\w+)&?", article_url).group(1),
        "idx": re.search(r"idx=(\d)&?", article_url).group(1),
    }


def get_qrcode_url_api(article_url="", **kwargs):
    """
    "mid": kwargs["mid"],
    "sn": kwargs["sn"],
    "idx": kwargs["idx"],
    """
    url_api = 'https://mp.weixin.qq.com/mp/qrcode?scene=10000005&'
    if article_url:
        return url_api + "&".join(k + "=" + v for k, v in split_article_url2mis(article_url).items())
    return url_api + "&".join(k + "=" + v for k, v in kwargs.items())



if __name__ == '__main__':
    pass
