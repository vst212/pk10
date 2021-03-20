# -*- coding: utf-8 -*-

import datetime
from collections import Counter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import MetaTrader5 as mt5
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from pandas import DataFrame


def loginmt5(account, password, server):
    """登录mt5返回实例"""
    # display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        return None

    # now connect to another trading account specifying the password
    account = account
    authorized = mt5.login(account, password=password, server=server)
    if authorized:
        # display trading account data 'as is'
        print(mt5.account_info())
        # display trading account data in the form of a list
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        print(account_info_dict)
        # for prop in account_info_dict:
        #     print("  {}={}".format(prop, account_info_dict[prop]))
        return mt5
    else:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
        return None


# shut down connection to the MetaTrader 5 terminal


class fuckmt5:
    """
    在一分钟内寻找点差最小的点进行交易
    """

    def __init__(self, mt5=None, symbol=None, maxdiancha=1000, lot=1.00, devitation=1000):
        self.mt5 = mt5
        self.symbol = symbol
        self.maxdiancha = maxdiancha
        self.lot = lot
        self.winnum = 0
        self.baselot = lot
        self.deviation = devitation
        self.last_low = 0
        self.last_high = 0

    def get_history(self, period=None, num=3, beishu=1000, pos=0):
        # 获取过去的bar从当前开始
        mt5 = self.mt5
        period = period or mt5.TIMEFRAME_M1
        rates = mt5.copy_rates_from_pos(self.symbol, period, pos, num)  # 从当前到过去10条记录

        newlist = [
            {"开盘": round(i[1], 5), "收盘": round(i[4], 5), "差价": round((i[4] - i[1]) * beishu, 2), "最高价": round(i[2], 5),
             "最低价": round(i[3], 5), "最大差价": round((i[2] - i[3]) * beishu, 2)

             }
            for i in rates]
        print("过去的记录:", newlist)
        return newlist

    def get_qujian(self, period=None):
        num = 2000
        his = self.get_history(num=num, period=period)
        tmplist = {}
        yingli = []
        kuisun = []
        chajia = []  # 使用累计算法  反向后重新计数
        is_up = False
        is_down = False
        tmpdown = 0
        tmpup = 0
        leiji = []
        for i in his:
            maxqujian = i['最高价'] - i['最低价']
            maxqujian = round(maxqujian * 1000, 5)
            if i["差价"] >= 0:
                maxchajia = i['收盘'] - i['开盘']
                maxchajia = round(maxchajia * 1000, 5)
                chajia.append(maxchajia)
                tmpup += maxchajia
                is_up = True
                # tmpdown = 0
                # if  is_up:
                leiji.append(tmpup)
                # 添加累计数

            if i["差价"] < 0:
                maxchajia = i['开盘'] - i['收盘']
                maxchajia = -round(maxchajia * 1000, 5)
                chajia.append(maxchajia)
                # tmpdown  += maxchajia
                tmpup += maxchajia
                is_down = True
                # tmpup =0
                # if is_down:
                leiji.append(tmpup)

            if maxqujian > 0.08:
                yingli.append(maxqujian)
            if maxqujian <= 0.08:
                kuisun.append(maxqujian)

        # yingli.sort()
        # kuisun.sort()
        tmplist["可盈利"] = yingli
        tmplist["亏损"] = kuisun

        # print(tmplist, len(yingli), len(kuisun), "盈利次数:%s" % (len(yingli) - len(kuisun)))
        #
        # print({"max": np.max(yingli), "min": np.min(yingli), "mean": np.mean(yingli)})
        #
        # print(chajia)
        # print({"正买曲线": chajia, "结果": sum(chajia)})
        ## 一小时的盈利均值 在1.4左右  最大值达到5.97  超过3为小概率事件了    最小盈利都有0.23

        # 柱状图
        df = pd.DataFrame({'yingli': yingli, "maxchajia": chajia, "zero": [0] * num, "leiji": leiji},
                          columns=['zero', 'leiji'])
        # df.plot.hist(bins=100)

        df.plot()  ## 默认是折线图   这是盈利曲线

        # 打印一个买入卖出的曲线

        # 累积折线图规律  如果某次翻转超过之前的幅度则继续跟进    正向幅度超过2.2 则购买反向

        # 看单次涨幅   超过某个点延续趋势  超过趋势极限点 翻转趋势   单次涨幅 + 累计涨幅综合评估 算出翻转点

        plt.show()

    def get_direct(self):
        history = self.get_history()
        close = history[1]['收盘']
        is_win = (history[1]['差价'] > 0 and history[0]['差价'] > 0) or (history[1]['差价'] < 0 and history[0]['差价'] < 0)

        if history[1]["差价"] > 0 and (history[1]["差价"] >= 0.3 or abs(history[1]["差价"] - history[0]["差价"]) >= 0.3):
            return ["sell", close, is_win]
        elif history[1]['差价'] < 0 and (history[1]["差价"] <= -0.3 or abs(history[1]["差价"] - history[0]["差价"]) >= 0.3):
            return ["buy", close, is_win]
        elif history[1]["差价"] > 0:
            return ["buy", close, is_win]
        elif history[1]["差价"] < 0:
            return ["sell", close, is_win]
        else:
            return {"balance", close, is_win}

    def buy(self):
        """
        市价买入函数，注意计算点差，点差太大不进行交易
        symbol:交易的品种 价格
        lots: 手数 0.01为迷你手
        deviation 买入允许最大价差
        """
        # 根据每个周期进行开仓平仓 统计价格
        mt5 = self.mt5
        symbol = self.symbol
        lot = self.lot
        deviation = self.deviation
        diancha = abs(mt5.symbol_info_tick(symbol).ask - mt5.symbol_info_tick(symbol).bid)
        if diancha < self.maxdiancha:
            """在固定点差范围内才进行买入 每秒钟检查一遍"""
            # point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                # "sl": price - 100 * point,  # 止损
                # "tp": price + 100 * point,  # 止盈
                "deviation": deviation,  # 开单价格波动
                "magic": 234000,  # 标识码
                "comment": "开仓买入！！",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # send a trading request
            result = mt5.order_send(request)
            print(result)
            # check the execution result
            print("1. 买入订单(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. 买入失败, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict = result._asdict()
                print(result_dict)
                if result.comment == 'Requote':
                    self.buy()
                # for field in result_dict.keys():
                #     print("   {}={}".format(field, result_dict[field]))
                #     # if this is a trading request structure, display it element by element as well
                #     if field == "request":
                #         traderequest_dict = result_dict[field]._asdict()
                #         for tradereq_filed in traderequest_dict:
                #             print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
                return None

            print("2. 买入成功, ", result)
            return result
        return None

    def sell(self):
        """
        市价卖出函数，注意计算点差，点差太大不进行交易
        symbol:交易的品种 价格
        lots: 手数 0.01为迷你手
        deviation 买入允许最大价差
        """
        # 根据每个周期进行开仓平仓 统计价格
        mt5 = self.mt5
        symbol = self.symbol
        lot = self.lot
        deviation = self.deviation
        diancha = abs(mt5.symbol_info_tick(symbol).ask - mt5.symbol_info_tick(symbol).bid)

        if diancha < self.maxdiancha:
            # point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).bid  # ask卖方的出价 bid买方出价
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                # "sl": price - 100 * point,  # 止损
                # "tp": price + 100 * point,  # 止盈
                "deviation": deviation,  # 开单价格波动
                "magic": 234000,  # 标识码
                "comment": "开仓卖出！！",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # send a trading request
            result = mt5.order_send(request)
            # check the execution result
            print("1. 卖出订单(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. 卖出失败, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict = result._asdict()
                print(result_dict)
                if result.comment == 'Requote':
                    self.sell()
                return None

            print("2. 卖出成功, ", result)
            return result
        return None

    def fill(self, result=None, lot=0.01):  # 这里应该是平掉所有的仓
        """
        平仓函数，注意计算点差，点差太大不进行交易
        symbol:交易的品种 价格
        lots: 手数 0.01为迷你手
        deviation 买入允许最大价差
        """
        # 根据每个周期进行开仓平仓 统计价格
        mt5 = self.mt5
        symbol = self.symbol
        deviation = self.deviation
        diancha = abs(mt5.symbol_info_tick(symbol).ask - mt5.symbol_info_tick(symbol).bid)
        # if diancha < self.maxdiancha:
        if result.request.type == mt5.ORDER_TYPE_BUY:
            deal_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        else:
            deal_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask

        position_id = result.order

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": deal_type,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "关闭订单！",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # send a trading request
        result2 = mt5.order_send(request)
        # check the execution result
        print("1. 平仓订单(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
        if result2.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. 平仓订单失败, retcode={}".format(result2.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result2._asdict()
            print(result_dict)
            self.fill(result, lot)
            return None

        print("2. 平仓订单成功, ", result2)
        return result2

    def open(self):
        """开新仓 平旧仓函数"""
        predict = self.get_direct()

        # 根据winnum判断是否加仓
        if predict[0] == "buy":
            result = self.buy()
            run_date = datetime.datetime.now() + datetime.timedelta(seconds=59)
            if result:
                print("开始平仓。。。。。")
                scheduler = BackgroundScheduler()
                scheduler.add_job(self.fill, 'date', run_date=run_date, args=[result, self.lot])
                scheduler.start()
        elif predict[0] == "sell":
            result = self.sell()
            run_date = datetime.datetime.now() + datetime.timedelta(seconds=59)
            if result:
                print("开始平仓。。。。。")
                scheduler = BackgroundScheduler()
                scheduler.add_job(self.fill, 'date', run_date=run_date, args=[result, self.lot])
                scheduler.start()

    def start(self):  # 定时器函数
        scheduler = BlockingScheduler()
        scheduler.add_job(self.open, 'cron', day_of_week='*', hour='*', minute="*", second=1, )
        scheduler.start()

    def test_qujian(self, period=None):
        num =  200 # 一个月
        his = self.get_history(num=num, period=period)
        his_pre = self.get_history(num=num+1, period=period)[0:-1]
        # print(his,"his------")
        tmplist = {}
        yingli = []
        kuisun = []
        chajia = []  # 使用累计算法  反向后重新计数
        is_up = False
        is_down = False
        tmpdown = 0
        tmpup = 0

        leiji = []
        predict_tmp = 0
        predict_res = []  ## 预测收益值得集合
        for index, i in enumerate(his):
            if index > 5:
                if i["差价"] >= 0:
                    maxchajia = i['最高价'] - i['最低价']
                    maxchajia = round(maxchajia * 1000, 5)

                    yingli.append(maxchajia)

                    chajia.append(maxchajia)
                    tmpup += maxchajia

                    rawlist = his[index - 5:index]
                    direct = self.predict_next(rawlist)
                    if direct and direct.get("direct"):
                        predict_tmp += maxchajia
                    elif direct and  not direct.get("direct"):
                        predict_tmp -= maxchajia
                    is_up = True

                    # tmpdown = 0
                    # if  is_up:
                    leiji.append(tmpup)
                    predict_res.append(predict_tmp)
                    # 添加累计数

                if i["差价"] < 0:
                    maxchajia = i['收盘'] - i['开盘']
                    maxchajia = round(maxchajia * 1000, 5)

                    yingli.append(maxchajia)

                    chajia.append(maxchajia)

                    tmpup += maxchajia

                    rawlist = his[index - 5:index]
                    direct = self.predict_next(rawlist)
                    if direct and direct.get("direct"):
                        predict_tmp += maxchajia
                    elif direct and  not direct.get("direct"):
                        predict_tmp -= maxchajia

                    # tmpup =0
                    # if is_down:
                    leiji.append(tmpup)  # 旧的累计曲线
                    predict_res.append(predict_tmp)

        # yingli.sort()
        # kuisun.sort()
        tmplist["可盈利"] = yingli
        tmplist["亏损"] = kuisun

        df = pd.DataFrame({'a': [i['收盘'] for i in his], "b":  [i['开盘'] for i in his],},
                          columns=[ 'a','b'])

        X = df['b']

        # 最高价  固定变量： 差价 最大差价 最高价 最低价  收盘价  开盘价    固定输出：  最大差价 差价 最高价 最低价 收盘价 比较两盘的方向i
        a =  [i['差价'] * 1000  for i in his_pre] # 起始的因
        b =  [i['差价'] * 1000 * (abs(his_pre[index]['差价'])/his_pre[index]['差价'])  for (index,i) in enumerate(his)]  # 想要的果
        self.show_relation(a,b)

        print(a,b)





        # df.plot.hist(bins=100)

        # df.plot.scatter(x='x', y='yingli')

        # df.plot()
        #
        # df.plot()  ## 默认是折线图   这是盈利曲线 area  bar
        # df2.plot()

        # 打印一个买入卖出的曲线

        # 累积折线图规律  如果某次翻转超过之前的幅度则继续跟进    正向幅度超过2.2 则购买反向

        # 看单次涨幅   超过某个点延续趋势  超过趋势极限点 翻转趋势   单次涨幅 + 累计涨幅综合评估 算出翻转点




    def show_relation(self,a,b):

        import statsmodels.api as smf  # 方法二
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        # est = smf.ols(formula='a ~ b', data=df).fit()  # 方法二
        # y_pred = est.predict(X)
        #
        # df['sales_pred'] = y_pred
        # print("sb66")
        #
        # print("回归结果jack", est.summary())  # 回归结果
        # print(est.params)  # 系数

        examdict = {"a":a,"b":b}

        examDf = DataFrame(examdict)

        rDf = examDf.corr()
        print(rDf)

        # plt.scatter(examDf.a, examDf.b, color='b', label="Exam Data")
        # plt.show()
        exam_X = examDf['a']
        exam_Y = examDf['b']

        X_train, X_test, Y_train, Y_test = train_test_split(exam_X, exam_Y, train_size=.6)
        # X_train为训练数据标签,X_test为测试数据标签,exam_X为样本特征,exam_y为样本标签，train_size 训练数据占比

        print("原始数据特征:", exam_X.shape,
              ",训练数据特征:", X_train.shape,
              ",测试数据特征:", X_test.shape)

        print("原始数据标签:", exam_Y.shape,
              ",训练数据标签:", Y_train.shape,
              ",测试数据标签:", Y_test.shape)

        plt.scatter(X_train, Y_train, color="blue", label="train data")
        # plt.scatter(X_test, Y_test, color="red", label="test data")  scatter

        model = LinearRegression()

        X_train = X_train.values.reshape(-1, 1)
        X_test = X_test.values.reshape(-1, 1)

        model.fit(X_train, Y_train)

        a = model.intercept_  # 截距

        b = model.coef_  # 回归系数

        print("最佳拟合线:截距", a, ",回归系数：", b)

        y_train_pred = model.predict(X_train)
        # 绘制最佳拟合线：标签用的是训练数据的预测值y_train_pred
        plt.plot(X_train, y_train_pred, color='black', linewidth=3, label="best line")

        # 测试数据散点图
        plt.scatter(X_test, Y_test, color='red', label="test data")

        # 添加图标标签
        plt.legend(loc=2)
        # 显示图像
        plt.show()

        score = model.score(X_test, Y_test)

        print(score)









    def predict_next(self, rawlist):
        nega = 0
        posi = 0

        rawlist = [i['差价'] for i in rawlist]

        for i in rawlist:
            if i > 0:
                posi += 1
            if i < 0:
                nega += 1
        total = sum(rawlist)

        ## 出现峰值得情况  波动很剧烈 价格上下波动 最终偏向大幅上升 # 这种情况价格会出现反转
        if posi - nega < 2 and total > 3:
            return {"direct": False}

        elif nega - posi < 2 and total < -3:
            return {"direct": True}

        ### 其他情况 单方面突进  价格跟随即可

        elif nega - posi >= 2:
            return {"direct": False}

        elif posi - nega >= 2:
            return {"direct": True}

        else:
            return None



# fuckmt5(mt5=mymt5,symbol="EURUSD").buy()

# 减少操作次数减少佣金  设置止盈止损条件
class Celue:
    win_count = 0

    money = 0

    winnum = 0

    def test(self, aclist, tips=0.03):
        for index, item in enumerate(aclist):  # 跟买500吧 赢51吧
            if index >= 1:
                if item['fx'] != aclist[index - 1]['fx']:
                    # if self.winnum == 3:  # 1分钟最佳是3
                    #     self.money += item['cj']  #* (2 ** (self.winnum))
                    #     self.winnum = 0
                    #     print("money:", round(self.money, 2))
                    # else:
                    #     self.money += item['cj'] #* (2 ** (self.winnum))
                    #     self.winnum += 1
                    self.money += item['cj']
                    print("money:", round(self.money, 2))
                else:
                    self.money -= item['cj']  # * (2 ** (self.winnum))
                    # self.winnum = 0
                    print("money:", round(self.money, 2))
        print({"实际盈利": round(round(self.money, 2) - round(len(aclist) * tips, 2), 2), "原始盈利:": round(self.money, 2),
               "手续费": round(len(aclist) * tips, 2), "耗时": "%s小时" % (len(aclist) // 60)})

    def count_cj(self, aclist):
        newlist = [i["cj"] for i in aclist]
        newlist2 = [i["fx"] for i in aclist]
        print(Counter(newlist), Counter(newlist2))

    def celue1(self, aclist, tips=0.03):  # 根据上一把的方向进行判断
        sxf = 0
        time = 0
        tztime = 0
        for index, item in enumerate(aclist):
            if index >= 2:
                if item['fx'] == "停止":
                    tztime += 1
                elif item['fx'] != aclist[index - 1]['fx']:
                    self.money += abs(item['cj'])
                    time += 1
                    sxf += 0.07
                    print("盈利:", abs(item['cj']))
                else:
                    self.money -= abs(item['cj'])
                    sxf += 0.07
                    time -= 1
                    print("亏损", abs(item['cj']))
        print({"盈利次数": time, "停止次数": tztime})
        print({"实际盈利": round(round(self.money, 2) - round(sxf, 2), 2), "原始盈利:": round(self.money, 2),
               "手续费": round(sxf, 2), "耗时": "%s小时" % (len(aclist) // 60)})

    def robot(self):

        pass

    def history_recorder(self, newpoint):
        """记录最高点最低点"""
        self.last_high = max(self.last_high, newpoint)
        self.last_low = max(self.last_low, newpoint)


def reform_list(rawlist):
    newlist = []
    for i in rawlist:
        if i['差价'] > 0:
            newlist.append({"fx": "买入", "cj": round((i["最高价"] - i['最低价']) * 1000, 2)})
        elif i['差价'] < 0:
            newlist.append({"fx": "卖出", "cj": round((i["最低价"] - i['最高价']) * 1000, 2)})
        else:
            newlist.append({"fx": "停止", "cj": i["差价"]})
    return newlist


mymt5 = loginmt5(account=50502883, password="ZAtUMRdF", server="ICMarketsSC-Demo")
# fuckmt5(mt5=mymt5, symbol="EURUSD").start()
fuckmt5(mt5=mymt5, symbol="EURUSD").test_qujian(mt5.TIMEFRAME_H2)

# 1小时买卖效果最佳 而且可以挂单 有足够长的时间获利


# rawlist = fuckmt5(mt5=mymt5, symbol="EURUSD").get_history(period=mymt5.TIMEFRAME_M1,num=200)
# newlist = reform_list(rawlist)
# # print("======================================================")
# guilv = CaiPiaoApi(token="").list_depart([i["fx"] for i in newlist])
# print([i["cj"] for i in newlist])
# print([ round(newlist[i -1]['cj'] - item["cj"],2) for i,item in enumerate(newlist) if i >=1 ])

# print(Counter(guilv))
# Celue().count_cj(newlist)
# Celue().celue1(newlist)


# 规则1 超过==0.3 价格就会反向  或价格改变比较上一次超过0.3


## 通过递增率 还有一个一分钟的最大差价来定是否会出现反弹！！！

# mymt2  = loginmt5(account="50502886",password="2Se5iG4G",server="ICMarketsSC-Demo")
# fuckmt5(mt5=mymt5, symbol="EURUSD").start()

# 获取未平仓的商品的价格
# biaodi = "EURUSD"
#
# positions = mt5.positions_get(symbol=biaodi)
# if not positions:
#     print("No positions on USDCHF, error code={}".format(mt5.last_error()))
# else:
#     print("Total positions on USDCHF =", len(positions))
#     # display all open positions
#     print("usdchf结果",positions)
#     # for position in positions:
#     #     print(position)


# request 1000 ticks from EURAUD
# euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020, 1, 28, 13), 1000, mt5.COPY_TICKS_ALL)
# # request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
# audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020, 1, 27, 13), datetime(2020, 1, 28, 13), mt5.COPY_TICKS_ALL)
#
# # get bars from different symbols in a number of ways
# eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020, 1, 28, 13), 1000)
# eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
# eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020, 1, 27, 13), datetime(2020, 1, 28, 13))
#
# # shut down connection to MetaTrader 5
# mt5.shutdown()
#
# # DATA
# print('euraud_ticks(', len(euraud_ticks), ')')
# for val in euraud_ticks[:10]: print(val)
#
# print('audusd_ticks(', len(audusd_ticks), ')')
# for val in audusd_ticks[:10]: print(val)
#
# print('eurusd_rates(', len(eurusd_rates), ')')
# for val in eurusd_rates[:10]: print(val)
#
# print('eurgbp_rates(', len(eurgbp_rates), ')')
# for val in eurgbp_rates[:10]: print(val)
#
# print('eurcad_rates(', len(eurcad_rates), ')')
# for val in eurcad_rates[:10]: print(val)
#
# # PLOT
# # create DataFrame out of the obtained data
# ticks_frame = pd.DataFrame(euraud_ticks)
# # convert time in seconds into the datetime format
# ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# # display ticks on the chart
# plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
# plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
#
# # display the legends
# plt.legend(loc='upper left')
#
# # add the header
# plt.title('EURAUD ticks')
#
# # display the chart
# plt.show()


# 获取某个品种的详情
# display EURJPY symbol properties
# symbol_info = mt5.symbol_info("EURUSD")
# if symbol_info != None:
#     # display the terminal data 'as is'
#     print(symbol_info)
#     print("EURUSD: spread =", symbol_info.spread, "  digits =", symbol_info.digits)
#     # display symbol properties as a list
#     print("Show symbol_info(\"EURUSD\")._asdict():")
#     symbol_info_dict = mt5.symbol_info("EURUSD")._asdict()
#     print(symbol_info_dict)
#     # for prop in symbol_info_dict:
#     #     print("  {}={}".format(prop, symbol_info_dict[prop]))


# symbol = "EURUSD"
# symbol_info = mt5.symbol_info(symbol)
# if symbol_info is None:
#     print(symbol, "not found, can not call order_check()")
#     mt5.shutdown()
#     quit()
#
# # if the symbol is unavailable in MarketWatch, add it
# if not symbol_info.visible:
#     print(symbol, "is not visible, trying to switch on")
#     if not mt5.symbol_select(symbol, True):
#         print("symbol_select({}}) failed, exit", symbol)
#         mt5.shutdown()
#         quit()