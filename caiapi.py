# 近100把的路数
import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from past.builtins import xrange

import readJSON
from collections import Counter
import random

class CaiPiaoApi:
    alllog = ""
    token = "SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D"
    # token =''
    baseprice = 100

    beishu = 2

    stopcount = 4
    price = 100
    yuer = 0
    nextbet = 0

    money = 0
    posi = True
    nega = False
    times = 0
    tmplist = []

    maxlose =0
    lose = 0

    sepcount = 12

    winnum = 0
    press_count =0

    def __init__(self, token):
        self.token = token

    def getluzhi(self):  # 历史记录
        self.money = 0
        self.times = 0
        newlist = []
        lenlist = []
        luzhiurl = "https://6970a.com/v/lottery/luzhi?gameId=45"
        res = requests.get(luzhiurl).json()[3]['luzhi']
        print(requests.get(luzhiurl).json()[3])
        for item in res:
            tmplist = item.split(',')
            lenlist.append(len(tmplist))
            newlist.extend(tmplist)
        # print(len(res), len(newlist))
        count = Counter(lenlist[::-1])
        sec = newlist
        count2 = Counter(sec)
        print(count2)
        print(Counter(lenlist))
        print(Counter(res))
        # print(newlist[50:60])
        count190 = Counter(sec[0:199])
        # print(count190.get('单'))
        # print(count190.get('双'))
        res = {"count2": count2, "count": count, "lenlist": lenlist[::-1], "rawlist": res[::-1], "newlist": sec}
        res2 = {"count2": count2, "count": count, "count199": count190, "count200": Counter(sec[190:200]),
                "lenlist": lenlist[::-1], "newlist": sec}

        self.moni2(rawlist=res['newlist'])

        # return self.judge2(rawlist=res['newlist'])

        # 跟买两把的正确率达到 200把大概100次机会  花费3个小时 获胜 最多连输50次   累计获胜50次  每次投注10 最终可获胜500  投注100次  -亏损 50*10*0.02 减去支出10块  最终获利
        # 490 3个小时

    def moni22(self,rawlist):
        self.money =0
        newlist = []

        dslist = ['单', '双']
        self.nextbet = ""

        # for index, current in enumerate(rawlist):
        #     print("nextbet,current",self.nextbet,current)
        #     if index >= 2:
        #         if self.nextbet == current:
        #             self.nextbet = rawlist[index - 2]
        #             if self.winnum == 3:
        #                 self.price = self.baseprice * (self.beishu  ** (self.winnum ))
        #                 self.money += self.price
        #                 self.winnum =0
        #             else:
        #                 self.price = self.baseprice * ( self.beishu ** (self.winnum ))
        #                 self.money += self.price
        #                 self.winnum +=1
        #             print("本次投注", self.price,"余额：",self.money)
        #         else:
        #             self.nextbet = rawlist[index - 2]
        #             self.money -= self.baseprice * (self.beishu ** (self.winnum ))
        #             # self.money -= self.price
        #             print("失败回到原点扣除", self.baseprice * (self.beishu ** (self.winnum )),"剩余：",self.money)
        #             self.winnum = 0
        #             self.price = self.baseprice
        print("最终余额",self.money)

    def judge22(self,rawlist):

        s = rawlist[-7]
        zero = rawlist[-6]
        current = rawlist[-5]
        next1 = rawlist[-4]
        next2 = rawlist[-3]
        next3 = rawlist[-2]
        next4 = rawlist[-1]

        arg1 = (s, zero, current, next1, next2, next3, next4)



        # 使用随机数进行购买
        dslist = [True, False]
        direction = random.choice(dslist)

        return {"bet": True, "direction": direction}

    def moni2(self, rawlist):
        newlist = []
        for index, current in enumerate(rawlist):
            if index <= len(rawlist) - 11:
                next1 = rawlist[index + 1]
                next2 = rawlist[index + 2]
                next3 = rawlist[index + 3]
                next4 = rawlist[index + 4]
                next5 = rawlist[index + 5]
                next6 = rawlist[index + 6]
                next7 = rawlist[index + 7]
                next8 = rawlist[index + 8]
                next9 = rawlist[index + 9]
                next10 = rawlist[index + 10]

                arg0 = (current, next1, next2, next3, next4, next5, next6, next7, next8, next9, next10)
                arg1 = (current, next1, next2, next3, next4, next5, next6, next7)
                arg2 = (current, next1, next2, next3, next4, next5)
                newlist.append(arg1)

                eqcount = self.judge_list(arg1)

                rvcount = 3 # 反转为5并不稳定
                # self.patter12(*arg1)
                # #
                # self.rdbet(*arg1)
                if eqcount > rvcount: # 说明不是趋势 用反马
                    self.lose = 0
                    self.fangmading(*arg1)

                if eqcount <= rvcount:
                    self.winnum = 0
                    self.mading(*arg1)

        # file = open('luz99i.txt', 'a')
        # file.write(
        #     "\n ----- \n" + str(Counter(newlist)) + '\n ---------------- \n' + str(
        #         {"money": self.money, "times": self.times}) + '\n ---------------- \n')
        with open("./mading.txt", mode='a') as file:
            file.write("\n"+ str({"money": self.money}) + "\n ----------------------------------")
        print({"money": self.money})

    # 根据短期的开奖记录切换方案

    def fangmading(self,*args):
        if len(args) >= 8:  # 模拟模式
            if args[6] == args[7]:
                if self.winnum == 3:
                    self.price = self.baseprice * (2  ** (self.winnum))
                    self.money += self.price
                    self.winnum = 0
                else:
                    self.price = self.baseprice * (2  ** (self.winnum ))
                    self.money += self.price
                    self.winnum += 1

                print("下一次投注", self.price,"余额：",self.money)
            else:
                self.money -= self.baseprice * (2  ** (self.winnum ))
                print("失败回到原点扣除", self.baseprice * (2  ** (self.winnum)),"剩余：",self.money)
                self.winnum = 0
                self.price = self.baseprice


    def mading(self,*args):
        if len(args) >= 8:  # 模拟模式
            if args[6] == args[7]: # 输的模式
                if self.lose == 3:
                    self.price = self.baseprice * (2  ** (self.lose))
                    self.money -= self.price
                    self.lose = 0
                else:
                    self.price = self.baseprice * (2  ** (self.lose ))
                    self.money -= self.price
                    self.lose += 1

                print("下一次投注", self.price,"余额：",self.money)
            else:
                self.money += self.baseprice * (2  ** (self.lose))
                print("失败回到原点扣除", self.baseprice * (2  ** (self.lose)),"剩余：",self.money)
                self.lose = 0
                self.price = self.baseprice



    def list_depart(self, c):
        a = []
        x = []
        y = []
        for i in range(0, len(c)):
            if i + 1 < len(c):
                if c[i] == c[i + 1]:
                    x.append(c[i])
                else:
                    x.append(c[i])
                    a.append(x)
                    x = []
            else:
                x.append(c[len(c) - 1])
                a.append(x)
        for i in a:
            y.append(tuple(i))
        print(y)
        return y

    def judge2(self, rawlist):
        #
        # s = rawlist[-7]
        # zero = rawlist[-6]
        # current = rawlist[-5]
        # next1 = rawlist[-4]
        # next2 = rawlist[-3]
        # next3 = rawlist[-2]
        # next4 = rawlist[-1]
        #
        # arg1 = ( s, zero, current, next1,next2,next3,next4)
        #
        # eqcount = self.judge_list(arg1)
        #
        # print("Eqcount", eqcount)
        #
        # rvcount = 4  # 反转为5并不稳定
        # #
        # # 使用随机数进行购买
        # dslist = [True,False]
        # direction = random.choice(dslist)

        return  {"bet": True, "direction": '单'}
        # if eqcount <= rvcount:
        #     # 反买
        #     print("反买")
        #     return self.patter12(*arg1)
        #
        # if eqcount > rvcount:
        #     # 正买
        #     print("正买")
        #     return self.patter13(*arg1)

    def patter12(self, *args):  # 反买
        # 对近5把进行判断

        self.times += 1
        if len(args) >= 8:  # 模拟模式
            if args[7] != args[6]:
                if self.winnum == 4:
                    self.price = self.baseprice * (2  ** (self.winnum ))
                    self.money += self.price
                    self.winnum =0
                else:
                    self.price = self.baseprice * ( 2 ** (self.winnum ))
                    self.money += self.price
                    self.winnum +=1

                print("本次投注", self.price,"余额：",self.money)
            else:
                self.money -= self.baseprice * (2 ** (self.winnum ))
                # self.money -= self.price
                print("失败回到原点扣除", self.baseprice * (2  ** (self.winnum )),"剩余：",self.money)
                self.winnum = 0
                self.price = self.baseprice

                # print("亏损100")
        else:  # 投注模式
            return {"bet": True, "direction": False}

    def patter13(self, *args):  # 正买
        """正买"""
        self.times += 1
        if len(args) >= 8:  # 模拟模式
            if args[6] == args[7]:
                if self.winnum == 4:
                    self.price = self.baseprice * (2  ** (self.winnum))
                    self.money += self.price
                    self.winnum = 0
                else:
                    self.price = self.baseprice * (2  ** (self.winnum ))
                    self.money += self.price
                    self.winnum += 1

                print("下一次投注", self.price,"余额：",self.money)
            else:
                self.money -= self.baseprice * (2  ** (self.winnum ))
                print("失败回到原点扣除", self.baseprice * (2  ** (self.winnum)),"剩余：",self.money)
                self.winnum = 0
                self.price = self.baseprice
                # print("亏损100")
        else:  # 投注模式
            return {"bet": True, "direction": True}

    def rdbet(self,*args):
        pass

    def judge_list(self, rawlist):
        eqcount = 0
        for index, item in enumerate(list(rawlist)):
            if index < len(rawlist) - 2:
                if item == rawlist[index + 1]:
                    eqcount += 1
        # print(rawlist, eqcount)
        return eqcount

    def judge_list_real(self, rawlist):
        eqcount = 0
        for index, item in enumerate(rawlist):
            if index < len(rawlist) - 1:
                if item == rawlist[index + 1]:
                    eqcount += 1
        return eqcount


    def touzhu(self):
        newyuer = self.getyuer()
        chajia = int(newyuer) - int(self.yuer)
        self.yuer = newyuer

        turn = self.getturn()
        kaijiang = self.kaijiang()
        # betinfo = kaijiang[0]
        mode = '单'
        alllog = kaijiang[2]

        self.press_count +=1

        self.price = self.baseprice

        if chajia > 0: # 这里修改价格 4轮为单位 单价为100 输光要20把
            if self.winnum == 3:
                self.winnum = 0
                self.price = self.baseprice * (2  ** (self.winnum))
            else:

                self.price = self.baseprice * (2  ** (self.winnum))
                self.winnum += 1
            self.maxlose = max([self.maxlose, self.lose])
            self.lose = 0

            print("投注价格翻倍",self.price)
            alllog += "累积盈利：%s把,累计耗时%s小时,最大损失%s把" % (self.winnum,round(self.press_count/60,2),self.maxlose)
        if chajia < 0:
            self.lose += 1
            self.winnum = 0
            self.price = self.baseprice
            alllog += "累积盈利：%s把,累计耗时%s小时,最大损失%s把" % (self.winnum,round(self.press_count/60,2),self.maxlose)
            print("投注价格不变", self.price)

        self.bet(turn, self.price, '单')
        # if not betinfo['bet']:
        #     return [self.yuer, turn, "不押注", alllog, self.price]
        # else:
        #     if betinfo['direction']:
        #         self.bet(turn, self.price, mode)
        #     elif mode == "单":
        #         mode = "双"
        #         self.bet(turn, self.price, mode)
        #     else:
        #         mode = "单"
        #         self.bet(turn, self.price, mode)

        return [self.yuer, turn, mode, alllog, self.price]

    def stop(self):
        scheduler = BlockingScheduler()
        scheduler.remove_job(job_id="666")

    def kaijiang(self):  # 开奖结果
        url = "https://6970a.com/js/anls-api/data/jssc60/numTrend/100.do"
        res = requests.get(url).json()['bodyList'][0:2]
        # print("开奖：", res)
        mylog = ""
        for index, openinfo in enumerate(res):
            if index == 0:
                qishu = openinfo["issue"]
                opentime = openinfo["openTime"]
                danshuang = self.format_odd(openinfo["openNum"][0])
                logstr = "开奖结果: 期数：%s  开奖时间：%s  <<%s>> \n" % (qishu, opentime, danshuang)
                mylog += logstr
        print(mylog)
        # isequal = (self.format_odd(res[0]["openNum"][0]) == self.format_odd(res[1]["openNum"][0]))
        betinfo = self.getluzhi()

        print("betinfo", betinfo)

        return [betinfo, self.format_odd(res[0]["openNum"][0]), mylog + "余额：<<%s>> " % str(self.yuer)]

    def bet(self, turnnum, price, mode):  # 押注api
        url = "https://6970a.com/api/bet"
        data = {"gameId": 45, "turnNum": str(turnnum), "content": [
            {"code": "45102102", "betInfo": mode, "odds": 1.98, "money": 1, "cateName": "冠军单双",
             "kyje": str(price * 1.98),
             "rebate": 0, "betModel": 0, "multiple": price, "totalMoney": str(price), "totalNums": 1}]}

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
            "Cookie": "md5Password=true; token=%s; JSESSIONID=EA674DD71084FDC50FCA6D7123DF4E1C" % self.token,
            "Referrer": "https://6970a.com/data/game/jssc60/index.html",
            "Origin": "https://6970a.com",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        res = requests.post(url, json=data, headers=headers).json()
        # print(headers, data, res)

    def start(self):  # 投注函数  根据上两期的结果进行投注 开完奖就投注 处理各种逻辑
        from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
        import  datetime
        file = open('./mading.txt', 'w')
        file.write('----mading----')

        scheduler = BlockingScheduler()
        scheduler.add_job(self.getluzhi, 'cron', next_run_time=datetime.datetime.now(), day_of_week='*', hour='*', minute="*", second="20",
                          id="666")  # 每分钟20秒的时候跑一次
        scheduler.start()

    def getyuer(self):
        url = "https://6970a.com/api/user/status"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
            "Cookie": "token=%s" % self.token
        }
        res = requests.get(url, headers=headers).json()
        print(res)
        return res['money']

    def getturn(self):  # 获取当前是第几盘
        url = "https://6970a.com/v/lottery/openInfo?gameId=45"
        res = requests.get(url).json()['cur']['turnNum']
        print(res)
        return res

    def format_odd(self, rawnum):
        if (int(rawnum) % 2) == 0:
            return "双"
        else:
            return "单"


# token=SpcQqiL%2FHt8ewpBISnsuDb2feV45t8pqGM%2BdluGs6eFb6YRVMqi8Cl20cN8RqsTYZ62dhQ%3D%3D; account=test403474; accountType=TEST
# Host: 6970a.com
# token=XdW%2Bm%2B%2FH%2FASJNS02Ngo5aO0qyubMKUspZRL9XKvbNYG8nEXxSCFf%2BFVaMXQe4auNpwbNJQ%3D%3D; account=test146018
# CaiPiaoApi(token="SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D").start()
# Rrwl4ZBMfkeWhj7cISeKmI0aAIa8M%2F%2B%2B%2B5Kp4anBF8fggxM1UuNsFAH9oVlq98dM35seZw%3D%3D; account=test540560
# CaiPiaoApi(token="B4NTh6NR99HrT0DULm4k%2F%2FrMWVUQdOPVmbneGREnXOx%2FgwRLkGVSZduulSQXWjk5ZBpvWg%3D%3D").touzhu()
# token=UCEOiZvl25Hb4qB7cyudUpwqOLw0ESqFAT67xrk%2F7y3ThdjZC0F49aIWJxqugFre7JYh5A%3D%3D; account=test127771; accountType=TEST
# md5Password=true; JSESSIONID=E45BB51D49CF5F51C6905E9632AA2299; token=jLOGhnQW%2F7vt87uZzQNzRz0oZ0%2F8uYpQvvXRNllh6t2pEVvt9gb%2BtzPBUwzmLFDKwkmPBA%3D%3D; account=test218477; accountType=TEST
# KEEq%2Bszl9swlfKh5LZXsdd2qiZ79cn953UjJaf4OgZpD%2FlPaDNYkWOSmtLoSYQdTSsS8Hg%3D%3D; account=test085444


