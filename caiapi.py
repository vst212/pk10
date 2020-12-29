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
    times = 0

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
        count190 = Counter(sec[0:199])
        print(count190.get('单'))
        print(count190.get('双'))
        res = {"count2": count2, "count": count, "lenlist": lenlist[::-1], "rawlist": res[::-1], "newlist": sec}
        res2 = {"count2": count2, "count": count, "count199": count190, "count200": Counter(sec[190:200]),
                "lenlist": lenlist[::-1], "newlist": sec}


        self.moni2(rawlist=res['newlist'])

        return self.judge2(rawlist=res['newlist'])

        # if count190.get('单') >= count190.get('双') + 3:
        #     print("买双", count190.get('双'), count190.get('单') - count190.get('双'))
        #
        #     return {"bet": True, "direction": '双'}
        #
        # else:
        #     print("买单", count190.get('双'), count190.get('单') - count190.get('双'))
        #
        #     return {"bet": True, "direction": '单'}

        # if count190.get('双') + 5 <= count190.get('单') <= count190.get('双') + 10 or count190.get('单') >= count190.get(
        #         '双') + 15:
        #     print("买双", count190.get('双'), count190.get('单') - count190.get('双'))
        #
        #     return {"bet": True, "direction": '双'}

        # elif count190.get('单') + 5 <= count190.get('双') <= count190.get('单') + 10 or count190.get('双') >= count190.get(
        #         '单') + 15:
        #     print("买单", count190.get('单'), count190.get('双') - count190.get('单'))
        #     return {"bet": True, "direction": '单'}
        # else:
        #     print("不买 单-双=", count190.get('单'), count190.get('双') - count190.get('单'))
        #     return {"bet": False, "direction": '单'}

        #moni_res = self.moni2(rawlist=res['newlist'])
        # print(res)
        # file = open('luz99i.txt', 'a')
        # file.write(
        #     '---------------- \n' + json.dumps(moni_res) + "\n ----- \n" + json.dumps(res2) + '\n ---------------- \n')
        # return self.judge(rawlist=res['newlist'])

        # 跟买两把的正确率达到 200把大概100次机会  花费3个小时 获胜 最多连输50次   累计获胜50次  每次投注10 最终可获胜500  投注100次  -亏损 50*10*0.02 减去支出10块  最终获利
        # 490 3个小时

    def moni(self, rawlist):  # 方案1

        realbet = 0
        betmoney = 100

        posi_counter =0
        nege_counter = 0   # 跟买2把 反买一把

        reverse_num  =0
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

                #
                # if  realbet >= 10:
                #     print("10kuai>",money)
                #     if current != next1:
                #         money +=1
                #         realbet += 1
                #         print("正向",money)
                #     if current == next1:
                #         money -= 1
                #         print("--反向---",money)
                #     if  realbet >=20:
                #         realbet = 0
                #
                # else:
                #     print("10小于")
                #     if current == next1:
                #         money +=1
                #         realbet +=1
                #         print("正向",money)
                #     if current != next1:
                #         money -= 1
                #         realbet -=1
                #         print("--反向---",money)



                # 顺势而为 稳
                # print("index",index)
                #
                # print(Counter(rawlist[index:index + final]))
                #
                # rest = self.calculate_times(rawlist[index:index + final])
                #
                # if not rest:
                #     times += 1
                #     if rawlist[index + final -1] == rawlist[index + final]:
                #         money += 1
                #     else:
                #         money -= 1
                # else:
                #     times += 1
                #     if rawlist[index + final -1] != rawlist[index + final]:
                #         money += 1
                #     else:
                #         money -= 1

                #===========去他妈的方案------------------------------
                # if  current != next1  and next1 !=next2 and next2!=next3:
                #     times += 1
                #     if next3 != next4:
                #         realbet += 1
                #         money += betmoney
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         # print("betmoney", betmoney)
                # #
                # if  current == next1  and next1 ==next2 and next2 ==next3:
                #     times += 1
                #     if next3 == next4:
                #         realbet += 1
                #         money += betmoney
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)
                #== == == == == =去他妈的方案 - -----------------------------

                ## 方案反买 连续反向趋势============================
                # if  current == next1  and next1 !=next2 and next2!=next3:
                #     times += 1
                #     if next3 == next4:
                #         realbet += 1
                #         money += betmoney
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         # print("betmoney", betmoney)


                # if current != next1 and next2 == next3 :
                #     times += 1
                #     if next3 == next4:
                #         realbet += 1
                #         money += betmoney
                #
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)


                ## =================================================
                ## 方案反买 连续反向趋势============================
                # if current == next1 and next1 == next2 and next2 != next3 and next4 != next5:
                #     times += 1
                #     if next6 != next5:
                #         realbet += 1
                #         money += betmoney
                #
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)

                # ## 方案反买 连续反向趋势============================  胜率最高
                # if current == next1 and next1 != next2 and next2 != next3 and next4 == next5:
                #     times += 1
                #     if next6 == next5:
                #         realbet += 1
                #         money += betmoney
                #
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)
                # ## =================================================
                #
                # if current != next1 and next1 == next2 and next2 == next3 and next5== next4:
                #     times += 1
                #     if next5 == next6:
                #         realbet += 1
                #         money += betmoney
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)


                # # 方案0------------------------- 目前最稳定
                # if  current == next1  and next1 !=next2:
                #     times += 1
                #     if next2 == next3:
                #         realbet += 1
                #         money += betmoney
                #         # print( "betmoney",betmoney)
                #     else:
                #         money -= betmoney
                #         realbet -= 1
                #         print("betmoney", betmoney)
                #
                # if current != next1 and next1 == next2:  ## 稳定
                #
                #     times += 1
                #
                #     if next2 == next3:
                #         realbet += 1
                #         money += betmoney
                #         # print("betmoney", betmoney)
                #     else:
                #         realbet -= 1
                #         money -= betmoney
                # print("betmoney", betmoney)
                # # 方案0-------------------------



                ## 方法6 ---------------------------------------
                # if current == next1 and next1 == next2 and next2 != next3:
                #     times += 1
                #     if next3 != next4:
                #         money += 1
                #         print(money)
                #     else:
                #         money -= 1
                #
                # if current != next1 and next1 != next2 and next2 == next3:
                #     times += 1
                #     if next3 == next4:
                #         money += 1
                #     else:
                #         money -= 1
                ## 方法6 ----------------------------------------------

                # if current == next1 and next1 != next2 and next3 != next2:  ## 稳定
                #     times += 1
                #     if next4 != next3:
                #         money += 1
                #     else:
                #         money -= 1

                # #方案一  13：16   11 71
                # if current == next1:  ## 稳定
                #     times += 1
                #     if next3 != next2:
                #         money += 1
                #     else:
                #         money -= 1
                # -----------------------------------------

                # betmoney = betmoney * 2
                # -------------------------------------------

                # if current == next1:
                #     times +=1
                #     if next1 != next2:
                #         money += 1
                #     else:
                #         money -= 1
                #     # betmoney = betmoney / 2
                # else:
                #     times += 1
                #     if next1 == next2:
                #         money += 1
                #     else:
                #         money -= 1
                #     # betmoney = betmoney * 2
                #     print( betmoney)

                # 稳定方案2

        print({ "money": self.money, "times": self.times})

    def moni2(self,rawlist):
        newlist = []
        for index, current in enumerate(rawlist):
            if index <= len(rawlist) - 7:
                next1 = rawlist[index + 1]
                next2 = rawlist[index + 2]
                next3 = rawlist[index + 3]
                next4 = rawlist[index + 4]
                next5 = rawlist[index + 5]
                next6 = rawlist[index + 6]

                arg1 = (current,next1,next2,next3,next4,next5)
                newlist.append(arg1)
                self.pattern1(*arg1)
                self.pattern2(*arg1)
                self.pattern3(*arg1)
               # --- self.pattern4(*arg1)
                self.pattern5(*arg1)
               # --- self.pattern6(*arg1)
                self.pattern7(*arg1)
                self.pattern8(*arg1)
                self.pattern9(*arg1)

        # print(Counter(newlist))
        file = open('luz99i.txt', 'a')
        file.write(
            "\n ----- \n" + str(Counter(newlist)) + '\n ---------------- \n' + str({"money": self.money, "times": self.times})+ '\n ---------------- \n' )
        print({"money": self.money, "times": self.times})


    # 根据短期的开奖记录切换方案

    def judge2(self,rawlist):
        current = rawlist[4]
        next1 = rawlist[3]
        next2 = rawlist[2]
        next3 = rawlist[1]
        next4 = rawlist[0]

        arg1 = (current, next1, next2, next3, next4)
        if self.pattern1(*arg1):
            print(self.pattern1(*arg1))
            return self.pattern1(*arg1)
        if self.pattern2(*arg1):
            return self.pattern2(*arg1)
        if self.pattern3(*arg1):
            return self.pattern3(*arg1)
        if self.pattern7(*arg1):
            return self.pattern7(*arg1)
        if self.pattern5(*arg1):
            return self.pattern5(*arg1)
        if self.pattern8(*arg1):
            return self.pattern8(*arg1)
        if self.pattern9(*arg1):
            return self.pattern9(*arg1)
        print("不压住")
        return {"bet": False, "direction": True}


    def pattern1(self,*args):  # 2 2 1 1 模式
        #组成新列表进行遍历
        if args[0] != args[1] and args[1] == args[2] and args[2] != args[3]  and args[3] == args[4]:
            self.times +=1
            if len(args) >= 6: #模拟模式
                if args[4] != args[5]:
                    self.money +=1
                else:
                    self.money -=1
            else: # 投注模式
                return {"bet": True, "direction": False}



    def pattern2(self,*args):  # 1 1 2 2  模式
        if args[0] != args[1] and args[1] != args[2] and args[2] == args[3]  and args[3] != args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] == args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": True}


    def pattern3(self,*args):  #  2 2  1 1 模式
        if args[0] == args[1] and args[1] != args[2] and args[2] == args[3]  and args[3] != args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] != args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": False}

    def pattern4(self,*args):  #  1  2  1 2  模式
        if args[0] != args[1] and args[1] == args[2] and args[2] != args[3]  and args[3] != args[4]:
            self.times +=1
            if args[4] == args[5]:
                self.money +=1
            else:
                self.money -=1


    def pattern5(self,*args):  #  4 1 1  模式
        if args[0] == args[1] and args[1] == args[2] and args[2] == args[3]  and args[3] != args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] != args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": False}

    def pattern6(self,*args):  #  2 1 1 1 1  模式
        if args[0] == args[1] and args[1] != args[2] and args[2] != args[3]  and args[3] != args[4]:
            self.times +=1
            if args[4] != args[5]:
                self.money +=1
            else:
                self.money -=1

    def pattern7(self,*args):  #  1 2 2  1   模式
        if args[0] != args[1] and args[1] == args[2] and args[2]  != args[3]  and args[3] == args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] != args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": False}

    def pattern8(self,*args):  #  1 3  2   模式
        if args[0] != args[1] and args[1] == args[2] and args[2]  == args[3]  and args[3] != args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] == args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": True}

    def pattern9(self,*args):  #  1  2  1  1  1 模式
        if args[0] != args[1] and args[1] == args[2] and args[2]  != args[3]  and args[3] != args[4]:
            self.times +=1
            if len(args) >= 6:  # 模拟模式
                if args[4] != args[5]:
                    self.money += 1
                else:
                    self.money -= 1
            else:  # 投注模式
                return {"bet": True, "direction": False}

    def calculate_times(self, rawlist):
        single = 0
        lianxu = 0
        print(rawlist)
        for index, current in enumerate(rawlist):
            if index < len(rawlist) - 1:
                if rawlist[index] == rawlist[index + 1]:
                    lianxu += 1
                else:
                    single += 1
        print(single - lianxu)
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
            # if chajia > 0:
            #     self.price = self.price * 2
            #     self.bet(turn, self.price, mode)
            # elif chajia < 0:
            #     self.price = self.price / 2
            #     self.bet(turn, self.price, mode)
            # else:
            #     self.bet(turn, self.price, mode)
            # if chajia >= 0:
            #     self.price = 100   # 固定100投注 输了减少投注
            #     self.bet(turn, self.price, betinfo['direction'])
            # elif chajia < 0:
            #     self.price = self.price / 2
            #     self.bet(turn, self.price, betinfo['direction'])
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

        print("betinfo",betinfo)

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

# JSESSIONID=52B9657AF18B2053E32F65BCF851CBEB; token=B4NTh6NR99HrT0DULm4k%2F%2FrMWVUQdOPVmbneGREnXOx%2FgwRLkGVSZduulSQXWjk5ZBpvWg%3D%3D; account=test015872; accountType=TEST
#kBUZicKjrK6YsTf1TkLPYquPpRLQEEghtfgFXMUqQyzgMYW%2Fef%2F1UT1C3IJ26anddWiz4w%3D%3D; account=test027325;

# token=Uo90hDBweO%2F2mZCVz7X2juoE40oMUTjyhd%2BBi3QShITH7sGVE9v0yI3BljZnYXfLXMUPcg%3D%3D; account=test821640; accountType=TEST
# 0YTvQY3DU18oqswIJeOEc5PXi20cvNs3TMN38ad3TAplp8GCFDfmHOKs9VsgtE5dkXeAFA%3D%3D
# test074803
# J38GqKbUkB1ZScGhbu0RgJfQB7YvcY0Fez6UHLsTqKUhHbM3xpVZ3FC%2Bo4ENne2knsAKbg%3D%3D
# CaiPiaoApi(token="SpIcyupj1luxw4jSkD2FBe25kLxRK2uaK0RD83C5wmLN6WRles3AOoWWeWaQ%2BBl3%2FX4uAA%3D%3D").touzhu()
# Rrwl4ZBMfkeWhj7cISeKmI0aAIa8M%2F%2B%2B%2B5Kp4anBF8fggxM1UuNsFAH9oVlq98dM35seZw%3D%3D; account=test540560
# CaiPiaoApi(token="B4NTh6NR99HrT0DULm4k%2F%2FrMWVUQdOPVmbneGREnXOx%2FgwRLkGVSZduulSQXWjk5ZBpvWg%3D%3D").touzhu()

