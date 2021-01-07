# 近100把的路数
import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

import readJSON
from collections import Counter


class CaiPiaoApi:
    alllog = ""
    token = "SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D"
    # token =''
    price = 100
    yuer = 0

    money = 0
    posi = True
    nega = False
    times = 0
    tmplist = []

    def __init__(self, token):
        self.token = token

    def getluzhi(self):  # 历史记录
        self.money = 0
        self.times = 0
        newlist = []
        lenlist = []
        luzhiurl = "https://6970a.com/v/lottery/luzhi?gameId=45"
        res = requests.get(luzhiurl).json()[3]['luzhi']
        print(res)
        for item in res:
            tmplist = item.split(',')
            lenlist.append(len(tmplist))
            newlist.extend(tmplist)
        # print(len(res), len(newlist))
        count = Counter(lenlist[::-1])
        sec = newlist
        count2 = Counter(sec)
        # print(newlist[50:60])
        count190 = Counter(sec[0:199])
        # print(count190.get('单'))
        # print(count190.get('双'))
        res = {"count2": count2, "count": count, "lenlist": lenlist[::-1], "rawlist": res[::-1], "newlist": sec}
        res2 = {"count2": count2, "count": count, "count199": count190, "count200": Counter(sec[190:200]),
                "lenlist": lenlist[::-1], "newlist": sec}

        self.moni2(rawlist=res['newlist'])

        return self.judge2(rawlist=res['newlist'])

        # 跟买两把的正确率达到 200把大概100次机会  花费3个小时 获胜 最多连输50次   累计获胜50次  每次投注10 最终可获胜500  投注100次  -亏损 50*10*0.02 减去支出10块  最终获利
        # 490 3个小时

    def moni(self, rawlist):  # 方案1

        realbet = 0
        betmoney = 100

        posi_counter = 0
        nege_counter = 0  # 跟买2把 反买一把

        reverse_num = 0
        for index, current in enumerate(rawlist):
            final = 20

            # len(rawlist) - final -1

            if index <= len(rawlist) - 7:
                next1 = rawlist[index + 1]
                next2 = rawlist[index + 2]
                next3 = rawlist[index + 3]
                next4 = rawlist[index + 4]
                next5 = rawlist[index + 5]
                next6 = rawlist[index + 6]

        print({"money": self.money, "times": self.times})

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

                arg1 = (current, next1, next2, next3, next4, next5, next6, next7, next8, next9, next10)
                newlist.append(arg1)

                eqcount = self.judge_list(arg1)

                # self.patter12(*arg1)

                if eqcount < 5:
                    # 反买
                    self.patter13(*arg1)

                if eqcount == 5:
                    self.patter12(*arg1)

                if eqcount > 5:
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

        arg1 = (t, n, e, s, zero, current, next1, next2, next3, next4,)

        eqcount = self.judge_list_real(arg1)

        print("Eqcount", eqcount)

        if eqcount < 5:
            # 反买
            return self.patter13(*arg1)

        if eqcount == 5:
            return self.patter12(*arg1)

        if eqcount > 5:
            return self.patter13(*arg1)

    def patter12(self, *args):  # 反买
        # 对近5把进行判断

        self.times += 1
        if len(args) >= 11:  # 模拟模式
            if args[9] != args[10]:
                self.money += 1
            else:
                self.money -= 1
        else:  # 投注模式
            return {"bet": True, "direction": False}

    def patter13(self, *args):  # 正买
        self.times += 1
        if len(args) >= 11:  # 模拟模式
            if args[9] == args[10]:
                self.money += 1
            else:
                self.money -= 1
        else:  # 投注模式
            return {"bet": True, "direction": True}

    def judge_list(self, rawlist):
        eqcount = 0
        for index, item in enumerate(rawlist):
            if index < len(rawlist) - 2:
                if item == rawlist[index + 1]:
                    eqcount += 1
        print(rawlist, eqcount)
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

    def judge(self, rawlist):
        prev4 = rawlist[3]
        prev3 = rawlist[2]
        prev2 = rawlist[1]
        prev1 = rawlist[0]

        if prev3 != prev2 and prev2 == prev1:  ## 正向投 胜率最稳定预测
            return {"bet": True, "direction": True}

        if prev3 == prev2 and prev2 != prev1:  ## 正向投 胜率最稳定预测
            return {"bet": True, "direction": True}

        # if prev3 != prev2 and prev2 != prev1:  ## 连续反向的 跟反向
        #     return {"bet": True, "direction": False}

        # if prev4 != prev3 and prev3 == prev2 and prev2 == prev1:  ## 正向投
        #     return {"bet": True, "direction": True}
        #
        # if prev4 == prev3 and prev3 != prev2 and prev2 != prev1:  ## 反向投
        #     return {"bet": True, "direction": False}

        # 连续3吧正确 第四把继续 稳定的打法

        return {"bet": False, "direction": True}

    def touzhu(self):
        newyuer = self.getyuer()
        chajia = int(newyuer) - int(self.yuer)
        self.yuer = newyuer
        turn = self.getturn()
        kaijiang = self.kaijiang()
        betinfo = kaijiang[0]
        mode = kaijiang[1]
        alllog = kaijiang[2]
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
#CaiPiaoApi(token="SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D").getluzhi()
# Rrwl4ZBMfkeWhj7cISeKmI0aAIa8M%2F%2B%2B%2B5Kp4anBF8fggxM1UuNsFAH9oVlq98dM35seZw%3D%3D; account=test540560
# CaiPiaoApi(token="B4NTh6NR99HrT0DULm4k%2F%2FrMWVUQdOPVmbneGREnXOx%2FgwRLkGVSZduulSQXWjk5ZBpvWg%3D%3D").touzhu()
# token=UCEOiZvl25Hb4qB7cyudUpwqOLw0ESqFAT67xrk%2F7y3ThdjZC0F49aIWJxqugFre7JYh5A%3D%3D; account=test127771; accountType=TEST
# md5Password=true; JSESSIONID=E45BB51D49CF5F51C6905E9632AA2299; token=jLOGhnQW%2F7vt87uZzQNzRz0oZ0%2F8uYpQvvXRNllh6t2pEVvt9gb%2BtzPBUwzmLFDKwkmPBA%3D%3D; account=test218477; accountType=TEST
#KEEq%2Bszl9swlfKh5LZXsdd2qiZ79cn953UjJaf4OgZpD%2FlPaDNYkWOSmtLoSYQdTSsS8Hg%3D%3D; account=test085444