# 近100把的路数
import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from past.builtins import xrange

import readJSON
from collections import Counter


class CaiPiaoApi:
    alllog = ""
    token = "SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D"
    # token =''
    baseprice = 100

    stopcount = 4
    price = 100
    yuer = 0

    money = 0
    posi = True
    nega = False
    times = 0
    tmplist = []

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

        # self.moni4(rawlist=res['newlist'])
        # self.moni3(rawlist=res['newlist'])

        # self.moni2(rawlist=res['newlist'])

        # self.genmai(rawlist=res['newlist'])
        # self.auto_reverse(rawlist=res['newlist'])

        return self.judge2(rawlist=res['newlist'])

        # 跟买两把的正确率达到 200把大概100次机会  花费3个小时 获胜 最多连输50次   累计获胜50次  每次投注10 最终可获胜500  投注100次  -亏损 50*10*0.02 减去支出10块  最终获利
        # 490 3个小时

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

                # self.zhengmai(*arg2)

                # self.patter12(*arg1)

                # self.shang5(*arg2)

                rvcount = 2 # 反转为5并不稳定
                #
                if eqcount <= rvcount:
                    # 反买
                    self.patter12(*arg1)

                if eqcount > rvcount:
                    # 正买
                    self.patter13(*arg1)

        #
        # print(self.tmplist)
        # print(Counter(self.tmplist))
        depart = self.list_depart(self.tmplist)
        # print("反向次数", len(depart))
        # print("------------------------- \n")
        # print(Counter(depart))
        # print(Counter(newlist))
        file = open('luz99i.txt', 'a')
        file.write(
            "\n ----- \n" + str(Counter(newlist)) + '\n ---------------- \n' + str(
                {"money": self.money, "times": self.times}) + '\n ---------------- \n')
        print({"money": self.money, "times": self.times})

    def moni3(self, rawlist):
        newlist = []
        num = self.sepcount  # 定义每组包含的元素个数
        for i in range(0, len(rawlist), num):
            newlist.append(rawlist[i:i + num])
        newlist = newlist[0:-1]
        print(newlist)
        for i in newlist:
            self.sixandsix(*tuple(i))
        print(len(newlist))
        print({"money": self.money, "times": self.times})

    def genmai(self, rawlist):  # 跟买n把 反转一把  继续跟买
        rvcount = 5
        for index, item in enumerate(rawlist):
            if index < len(rawlist) - 1:
                if (index % rvcount) != 0:
                    if item == rawlist[index + 1]:
                        self.money += 1
                    else:
                        self.money -= 1
                else:
                    if item != rawlist[index + 1]:
                        self.money += 1
                    else:
                        self.money -= 1
        print("money:", self.money)

    def auto_reverse(self, rawlist):  # 自动反转  买对了跟买 买错了反买
        fanmai = False
        losecount = 0
        rvcount = 1
        for index, item in enumerate(rawlist):
            if index < len(rawlist) - 1:
                if not fanmai:
                    if item == rawlist[index + 1]:
                        self.money += 1
                        losecount -= 1
                    else:
                        self.money -= 1
                        losecount += 1
                        if losecount > rvcount:
                            fanmai = True
                else:
                    if item != rawlist[index + 1]:
                        self.money += 1
                        losecount -= 1
                    else:
                        self.money -= 1
                        losecount += 1
                        if losecount > rvcount:
                            fanmai = False
        print("money:", self.money)

    def shang5(self, *args):
        self.times += 1

        # count = Counter(args[0:-1]).get("单") - Counter(args[0:-1]).get("双")
        # print( count)
        if len(args) >= 6:  # 模拟模式
            if Counter(args[0:-1]).get("单") and Counter(args[0:-1]).get("单") >= 0:
                if args[5] == "单":
                    self.money += 1
                else:
                    self.money -= 1
            elif Counter(args[0:-1]).get("双") and Counter(args[0:-1]).get("双") >= 100:
                if args[5] == "双":
                    self.money += 1
                else:
                    self.money -= 1
        else:  # 投注模式
            return {"bet": True, "direction": False}

    # 根据短期的开奖记录切换方案

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
        return y

    def judge2(self, rawlist):
        t = rawlist[-10]
        n = rawlist[-9]
        e = rawlist[-8]
        s = rawlist[-7]
        zero = rawlist[-6]
        current = rawlist[-5]
        next1 = rawlist[-4]
        next2 = rawlist[-3]
        next3 = rawlist[-2]
        next4 = rawlist[-1]

        arg1 = (t, n, e, s, zero, current, next1,)

        eqcount = self.judge_list(arg1)

        print("Eqcount", eqcount)

        rvcount = 2  # 反转为5并不稳定
        #
        if eqcount <= rvcount:
            # 反买
            return self.patter12(*arg1)

        if eqcount > rvcount:
            # 正买
            return self.patter13(*arg1)

    def sixandsix(self, *args):
        # 12个数据 每12个作为一次预测！
        arg1 = args[0:int(self.sepcount / 2)]
        arg2 = args[int(self.sepcount / 2):]
        eqcountprev = self.judge_list(arg1)

        eqcountnext = self.judge_list(arg2)

        # print(eqcountnext,eqcountprev)

        if eqcountprev > self.sepcount - 1:
            # 如果前面6把正买比较多  直接正买在未来6把
            self.money += eqcountnext - (int(self.sepcount / 2) - 1 - eqcountnext)
        else:
            self.money += int(self.sepcount / 2) - 1 - eqcountnext - eqcountnext

    def moni4(self, rawlist):
        # 12个数据 每12个作为一次预测！

        newlist = []
        num = 6  # 定义每组包含的元素个数
        for i in range(0, len(rawlist), num):
            newlist.append(rawlist[i:i + num])
        newlist = newlist[0:-1]

        for index, item in enumerate(newlist):
            if index < len(newlist) - 1:
                arg1 = tuple(item)
                arg2 = tuple(newlist[index + 1])

                eqcountprev = self.judge_list(arg1)

                eqcountnext = self.judge_list(arg2)

                # print(eqcountnext,eqcountprev)

                if eqcountprev > 4:
                    # 如果前面6把正买比较多  直接正买在未来6把
                    self.money += eqcountnext - (5 - eqcountnext)
                else:
                    self.money += 5 - eqcountnext - eqcountnext
        print({"money": self.money, "times": self.times})

    def zhengmai(self, *args):

        self.press_money = 1
        if len(args) >= 4:  # 模拟模式
            if args[0] != args[1]:

                if args[1] == args[2]:
                    self.times += 1
                    self.money += self.press_money
                    self.press_money = 1
                else:
                    self.money -= self.press_money
                    self.press_money = 2
            # elif args[0] == args[1]:
            #     if args[1] != args[2]:
            #         self.money += 1
            #     else:
            #         self.money -= 1
        else:  # 投注模式
            return {"bet": True, "direction": False}

    def patter12(self, *args):  # 反买
        # 对近5把进行判断

        self.times += 1
        if len(args) >= 8:  # 模拟模式
            if args[7] != args[6]:
                self.winnum +=1
                self.price = self.baseprice * (2 ** (self.winnum - 1))
                self.money += self.price
                if self.winnum == 4:
                    self.winnum =0
                    self.price =self.baseprice
            else:
                self.winnum = 0
                self.money -= self.baseprice
                self.price = self.baseprice
                # print("亏损100")
        else:  # 投注模式
            return {"bet": True, "direction": False}

    def patter13(self, *args):  # 正买
        """正买"""
        self.times += 1
        if len(args) >= 8:  # 模拟模式
            if args[6] == args[7]:
                self.winnum += 1
                self.price = self.baseprice * (2 ** (self.winnum -1))
                self.money += self.price
                if self.winnum == 4:
                    self.winnum =0
                    self.price = self.baseprice
            else:
                self.winnum = 0
                self.money -= self.baseprice
                self.price = self.baseprice
                # print("亏损100")
        else:  # 投注模式
            return {"bet": True, "direction": True}

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

    def calculate_times(self, rawlist):
        single = 0
        lianxu = 0
        for index, current in enumerate(rawlist):
            if index < len(rawlist) - 1:
                if rawlist[index] == rawlist[index + 1]:
                    lianxu += 1
                else:
                    single += 1
        return single - lianxu > 0 and False or True

    def get_percent(self, rawlist):
        return 6

    def touzhu(self):
        newyuer = self.getyuer()
        chajia = int(newyuer) - int(self.yuer)
        self.yuer = newyuer

        turn = self.getturn()
        kaijiang = self.kaijiang()
        betinfo = kaijiang[0]
        mode = kaijiang[1]
        alllog = kaijiang[2]

        self.press_count +=1


        if chajia > 0: # 这里修改价格 4轮为单位 单价为100 输光要20把
            self.winnum += 1
            self.price = self.baseprice * (2 ** (self.winnum - 1))
            if self.winnum == 4:
                self.winnum = 0
                self.price = self.baseprice
            alllog += "累积盈利：%s把,累计耗时%s小时" % (self.winnum,round(self.press_count/60,2))
        if chajia < 0:
            self.winnum = 0
            self.price = self.baseprice
            alllog += "累积盈利：%s把，累计耗时%s小时" % (self.winnum,round(self.press_count/60,2))

        if not betinfo['bet']:
            return [self.yuer, turn, "不押注", alllog, self.price]
        else:
            if betinfo['direction']:
                self.bet(turn, self.price, mode)
            elif mode == "单":
                mode = "双"
                self.bet(turn, self.price, mode)
            else:
                mode = "单"
                self.bet(turn, self.price, mode)

        return [self.yuer, turn, mode, alllog, self.price]

    def stop(self):
        scheduler = BlockingScheduler()
        scheduler.remove_job(job_id="666")

    def kaijiang(self):  # 开奖结果
        url = "https://6970a.com/js/anls-api/data/jssc60/numTrend/100.do"
        res = requests.get(url).json()['bodyList'][0:2]
        print("开奖：", res)
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
CaiPiaoApi(token="SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D").getluzhi()
# Rrwl4ZBMfkeWhj7cISeKmI0aAIa8M%2F%2B%2B%2B5Kp4anBF8fggxM1UuNsFAH9oVlq98dM35seZw%3D%3D; account=test540560
# CaiPiaoApi(token="B4NTh6NR99HrT0DULm4k%2F%2FrMWVUQdOPVmbneGREnXOx%2FgwRLkGVSZduulSQXWjk5ZBpvWg%3D%3D").touzhu()
# token=UCEOiZvl25Hb4qB7cyudUpwqOLw0ESqFAT67xrk%2F7y3ThdjZC0F49aIWJxqugFre7JYh5A%3D%3D; account=test127771; accountType=TEST
# md5Password=true; JSESSIONID=E45BB51D49CF5F51C6905E9632AA2299; token=jLOGhnQW%2F7vt87uZzQNzRz0oZ0%2F8uYpQvvXRNllh6t2pEVvt9gb%2BtzPBUwzmLFDKwkmPBA%3D%3D; account=test218477; accountType=TEST
# KEEq%2Bszl9swlfKh5LZXsdd2qiZ79cn953UjJaf4OgZpD%2FlPaDNYkWOSmtLoSYQdTSsS8Hg%3D%3D; account=test085444


import random

WIN  = 1
LOSE = 0

def gambling_50_percent(pocket, pay):
    result = random.randint(0, 1)
    if result == WIN:
        pocket += pay
    else:
        pocket -= pay
    return result, pocket

def play_a_round(win_time_to_stop, pocket, pay, n):
    money_when_start = pocket
    root_pay = pay

    for i in xrange(win_time_to_stop):
        win_or_lose, pocket = gambling_50_percent(pocket, pay)
        if win_or_lose == WIN:
            pay *= n
        else:
            pay = root_pay
            break
    # print(pocket, pay)
    return pocket - money_when_start, pocket > money_when_start

# mymoney = 0
# for i in range(20000):
#     mymoney += play_a_round(5,2000,200,2)[0]
#
# print(mymoney)

##token=AN1XWoTSYHUYzVnQwIETpDFv6WmhS3cMb2Kj1cnd5zsnUT%2FYSdfIYBQzJGJ2r245GM%2BkZQ%3D%3D; account=test061820; accountType=TEST