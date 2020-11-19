
from telegram.ext import Updater
import logging
import requests
import json
import random
import os
from pyquery import PyQuery as pq
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import re
import util
import gc
s=requests
import readJSON


proxy={"http":"127.0.0.1:8080"}
proxy2="https:127.0.0.1:8080"
# t = Twitter(auth=OAuth(OAUTH_TOKEN , OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET),format="json") 

配置= readJSON.读JSON文件("config.json")
用户表=配置["user"]
旧进度=配置["currentupload"] 
新进度=配置["currentupload"]  ##上传的进度  


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

id="@jurufuli"
#id="@testme66av"
updater = Updater(token='1196273795:AAFWSG6wNd9tLKtJk1fwxNuEgLr2T75VVXk', use_context=True)
dispatcher = updater.dispatcher


def sendmsg(msg):
    updater.bot.send_message(id, text=msg)


def sendphoto(url):
    updater.bot.send_photo(id, photo=url)




def store_last_id(tweet_id):
    with open('lastid', 'w') as fp:
        fp.write(str(tweet_id))


def get_last_id():
    with open('lastid') as fp:
        return fp.read()







def search(): #随机抓取
    url="http://nastypornpics.com/search/big-tits/%s/"
    header={"Cache-Control": "no-cache",
            "Pragma": "no-cache",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
           "Upgrade-Insecure-Requests": "1","Cookie": "36a2e64d494bd0d256c0b9a11558befb855eb4380396ede6673=ZE5sUmUyNXRoUzlVd3FScDVZSDUzc3pzdm9GMzljdFNPVEk0TXpFM09UazNOalpoTlRnM056VTBaR016TWpRd01UZGlNRFpsWVRjPQc; af4bfc66a546d1ee1fc87c1c2f1eb2c43e9fcfdf9cb893bf92fe8bfbb2c7eb87=ZnV6M0gwMjlBTVRZd05ERTVNamt3Tnkwd0xUST0b; ftt2_first=1; 93e07b1337f73139e4c955c5d2aa5a7e21830264c9e1952ed1c685624e=RjZCZGEwOWt4MnNTZ1l1Zk1TMHcb; ftt2=eyJpcCI6MzIyMTQ4NjQ0NSwiZiI6MCwicyI6InNlIiwidiI6WyIyNzYiXSwiY2MiOjIsImluIjoxfQ%3D%3D","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
    result=s.get(url%(新进度)).text
    html=pq(result)
    ##默认的保存列表
    data=[]
    #修改内容处获取列表的地方
    li=html("#container").find('li').items()
    for item  in li:
        #print("nissad")
        try:
            link=item('img').attr('data-src')  #.split("/")[lsloc]
            data.append(link)
        except Exception as e:
            pass    
    print(data)    
    return data


def 单次发送():
    global 新进度
    datalist=search()
    新表=util.qiefen(datalist,2)
    for i in 新表:
        for ii in i:
            sendphoto("https://66avvv.com/pic.php?p="+ii)
            print("发射照片!")
        time.sleep(1200)        
    新进度+=1
    print("用户%s发送完毕，更新进度为%s"%(username,新进度))
    配置["currentupload"]+=1
    print("更新上传进度为%s"%(配置["currentupload"]))
    readJSON.writejson("config.json",配置)   ##发送完写入进入

def 循环发送():
    print("开始每日计划任务啦·干就完啦！")
    scheduler = BlockingScheduler() 
    scheduler.add_job(单次发送, 'interval', minutes=160,next_run_time=datetime.datetime.now())  ##每隔6小时推一次  
    scheduler.start()   


#search()
#单次发送()
循环发送()
input()