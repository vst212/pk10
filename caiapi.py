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
    yuer = ""

    def __init__(self, token):
        self.token = token

    def getluzhi(self):  # 历史记录
        newlist = []
        lenlist = []
        luzhiurl = "https://6970a.com/v/lottery/luzhi?gameId=45"
        res = requests.get(luzhiurl).json()[3]['luzhi']
        for item in res:
            tmplist = item.split(',')
            lenlist.append(len(tmplist))
            newlist.extend(tmplist)
        print(len(res), len(newlist))
        count = Counter(lenlist[::-1])
        sec = newlist[::-1]
        count2 = Counter(sec)
        # print(newlist[50:60])
        res = {"count2": count2, "count": count, "lenlist": lenlist[::-1], "rawlist": res[::-1], "newlist": sec}
        res2 = {"count2": count2, "count": count, "lenlist": lenlist[::-1]}
        moni_res = self.moni(rawlist=res['newlist'])
        print(res2)
        file = open('./luzi.txt', 'a')
        file.write(
            '---------------- \n' + json.dumps(moni_res) + "\n ----- \n" + json.dumps(res2) + '\n ---------------- \n')
        return self.judge(rawlist=res['newlist'])

        # 跟买两把的正确率达到 200把大概100次机会  花费3个小时 获胜 最多连输50次   累计获胜50次  每次投注10 最终可获胜500  投注100次  -亏损 50*10*0.02 减去支出10块  最终获利
        # 490 3个小时

    def moni(self, rawlist):  # 方案1
        money = 0
        times = 0
        for index, current in enumerate(rawlist):
            if index <= (len(rawlist) - 5):
                next1 = rawlist[index + 1]
                next2 = rawlist[index + 2]
                next3 = rawlist[index + 3]
                next4 = rawlist[index + 4]
                # next5 = rawlist[index + 5]
                # 顺势而为 稳

                # # 方案0
                if  current == next1  and next1 !=next2:
                    times += 1
                    if next2 == next3:
                        money +=1
                    else:
                        money -=1

                if current != next1 and next1 == next2:  ## 稳定

                    times += 1

                    if next2 == next3:

                        money += 1

                        # if next4 == next3:
                        #     money += 1
                        # else:
                        #     money -= 1

                    else:
                        money -= 1

                # elif current == next1 and next1 != next2 and next3 != next2:  ## 稳定
                #     times += 1
                #     if next4 != next3:
                #         money += 1
                #     else:
                #         money -= 1

                # 方案一  13：16   11 71
                # if current == next1:  ## 稳定
                #     times += 1
                #     if next3 != next2:
                #         money += 1
                #     else:
                #         money -= 1

                # 稳定方案2

        print( {"money": money, "times": times})
        return {"money": money, "times": times}

    # 根据短期的开奖记录切换方案

    def judge(self, rawlist):
        prev4 = rawlist[3]
        prev3 = rawlist[2]
        prev2 = rawlist[1]
        prev1 = rawlist[0]

        if prev3 != prev2 and prev2 == prev1:  ## 正向投 胜率最稳定预测
            return {"bet": True, "direction": True}

        if prev3 == prev2 and prev2 != prev1:  ## 正向投 胜率最稳定预测
            return {"bet": True, "direction": True}


        # if prev4 != prev3 and prev3 == prev2 and prev2 == prev1:  ## 正向投
        #     return {"bet": True, "direction": True}
        #
        # if prev4 == prev3 and prev3 != prev2 and prev2 != prev1:  ## 反向投
        #     return {"bet": True, "direction": False}



        # 连续3吧正确 第四把继续 稳定的打法

        return {"bet": False, "direction": True}

    def touzhu(self):
        self.yuer = self.getyuer()
        turn = self.getturn()
        kaijiang = self.kaijiang()
        betinfo = kaijiang[0]
        mode = kaijiang[1]
        alllog = kaijiang[2]
        if not betinfo['bet']:
            return [self.yuer, turn, "不押注", alllog]
        else:
            if betinfo['direction']:
                self.bet(turn, self.price, mode)
            elif mode == "单":
                mode = "双"
                self.bet(turn, self.price, mode)
            else:
                mode = "单"
                self.bet(turn, self.price, mode)

        return [self.yuer, turn, mode, alllog]

    def stop(self):
        scheduler = BlockingScheduler()
        scheduler.remove_job(job_id="666")

    def kaijiang(self):  # 开奖结果
        url = "https://6970a.com/js/anls-api/data/jssc60/numTrend/100.do"
        res = requests.get(url).json()['bodyList'][0:2]
        mylog = ""
        for openinfo in res:
            qishu = openinfo["issue"]
            opentime = openinfo["openTime"]
            danshuang = self.format_odd(openinfo["openNum"][0])
            logstr = "开奖结果: 期数：%s  开奖时间：%s  <<%s>> \n" % (qishu, opentime, danshuang)
            mylog += logstr
        print(mylog)
        # isequal = (self.format_odd(res[0]["openNum"][0]) == self.format_odd(res[1]["openNum"][0]))
        betinfo = self.getluzhi()

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
        print(headers, data, res)

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


# test074803
# J38GqKbUkB1ZScGhbu0RgJfQB7YvcY0Fez6UHLsTqKUhHbM3xpVZ3FC%2Bo4ENne2knsAKbg%3D%3D
# CaiPiaoApi(token="SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D").touzhu()
CaiPiaoApi(token="J38GqKbUkB1ZScGhbu0RgJfQB7YvcY0Fez6UHLsTqKUhHbM3xpVZ3FC%2Bo4ENne2knsAKbg%3D%3D").getluzhi()
