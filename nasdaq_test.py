# -*- coding: utf-8 -*-
import json

import requests

# 纳斯达克指数一分钟

interval = 60 # 1分钟  60   900 15分钟 1800 30分钟 5分钟300


url = "https://tvc4.forexpros.com/ae23b9450215d31476937c5f404c96a0/1616229560/6/6/28/history?symbol=8874&resolution=60&from=1605861727&to=1616229787"

payload = {}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,th;q=0.6,fr;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://tvc-cncdn.investing.com/',
    'Origin':'https://tvc-cncdn.investing.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# response = requests.request("GET", url, headers=headers, data=payload).json()
# f= open("nas100.json",'w')
# f.write(json.dumps(response))
# print(response)

# newlist = [ i[1] for i  in response]
# print(newlist)
#
# # 判断差价  每次都从收盘价开始买入   判断趋势
#
# aclist = []
# fxlist = []
#
# for index,item  in enumerate(newlist):
#     if index >= 1:
#         cj = round(item - newlist[index-1],2)
#         # pre_cj = newlist[index-1]  - newlist[index-2]
#         if cj<0:
#             aclist.append({"cj":abs(cj),'fx':"卖出"})
#             fxlist.append("卖出")
#         elif cj == 0:
#             aclist.append({"cj":abs(cj),'fx':"持平"})
#             fxlist.append("持平")
#         elif cj >0:
#             aclist.append({"cj": abs(cj), 'fx': "买入"})
#             fxlist.append("买入")
#
# # print(aclist)
# # print(fxlist)
#
# init_money = 0  # 初始资金100美金  # 买迷你手预付款13  每次赚的就是差价
#
#
# # 计算跟买的胜率
#
#
#
# class Celue:
#     win_count = 0
#
#     money = 0
#
#     winnum = 0
#
#     def test(self,aclist):
#         for index,item  in enumerate(aclist):  # 跟买500吧 赢51吧
#             if index >= 1:
#                 if item['fx'] == aclist[index -1]['fx']:
#                     if self.winnum == 3:  # 1分钟最佳是3
#                         self.money += item['cj'] * (2 ** (self.winnum))
#                         self.winnum = 0
#                         print("money:", round(self.money, 2))
#                     else:
#                         self.money += item['cj'] * (2 ** (self.winnum))
#                         self.winnum += 1
#                         print("money:", round(self.money, 2))
#                 else:
#                     self.money -= item['cj'] * (2 ** (self.winnum))
#                     self.winnum = 0
#                     print("money:", round(self.money, 2))
#         print("money:",round(self.money,2))
#         print(len(aclist))


# Celue().test(aclist)

