# -*- coding: utf-8 -*-
import requests

# 纳斯达克指数一分钟

interval = 60 # 1分钟  60   900 15分钟 1800 30分钟 5分钟300


url = "https://cn.investing.com/common/modules/js_instrument_chart/api/data.php?" \
      "pair_id=14958&pair_id_for_news=14958&chart_type=area&pair_interval=%s&" \
      "candle_count=500&events=yes&volume_series=yes&period=" % interval

payload = {}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,th;q=0.6,fr;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'adBlockerNewUserDomains=1612631623; adsFreeSalePopUp=3; udid=12be990fa8ec9c89f3451e19f78f6d0e; G_ENABLED_IDPS=google; geoC=CN; PHPSESSID=shu7e81jt4akqjdl0q3jerjf5e; StickySession=id.57929901230.609cn.investing.com; logglytrackingsession=f1f0b05e-a588-418b-94f7-c48d1408f06b; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%222%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A13%3A%22%E8%8B%B1%E9%95%91+%E7%BE%8E%E5%85%83%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fgbp-usd%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%221%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A13%3A%22%E6%AC%A7%E5%85%83+%E7%BE%8E%E5%85%83%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Feur-usd%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22941155%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fequities%2Falibaba%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228836%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcommodities%2Fsilver%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2214958%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A25%3A%22%2Findices%2Fnasdaq-composite%22%3B%7D%7D%7D%7D; nyxDorf=ZGUyY2MrMW8yYGFoYi9hYWIwM2o3LmFgNTQ%3D; nyxDorf=MTA0ZTV9NWsxY2xlNXg1NT9tMmszKjMyNzY%3D',
    'Host': 'cn.investing.com',
    'Pragma': 'no-cache',
    'Referer': 'https://cn.investing.com/indices/nasdaq-composite',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.request("GET", url, headers=headers, data=payload).json()['candles']

# print(response)

newlist = [ i[1] for i  in response]
# print(newlist)

# 判断差价  每次都从收盘价开始买入   判断趋势

aclist = []
fxlist = []

for index,item  in enumerate(newlist):
    if index >= 1:
        cj = round(item - newlist[index-1],2)
        # pre_cj = newlist[index-1]  - newlist[index-2]
        if cj<0:
            aclist.append({"cj":abs(cj),'fx':"卖出"})
            fxlist.append("卖出")
        elif cj == 0:
            aclist.append({"cj":abs(cj),'fx':"持平"})
            fxlist.append("持平")
        elif cj >0:
            aclist.append({"cj": abs(cj), 'fx': "买入"})
            fxlist.append("买入")

# print(aclist)
# print(fxlist)

init_money = 100  # 初始资金100美金  # 买迷你手预付款13  每次赚的就是差价


# 计算跟买的胜率



class Nas:
    win_count = 0

    money = 0

    winnum = 0

    def test(self,aclist):
        for index,item  in enumerate(aclist):  # 跟买500吧 赢51吧
            if index >= 1:
                if item['fx'] == aclist[index -1]['fx']:
                    if self.winnum == 3:  # 1分钟最佳是3
                        self.money += item['cj'] * (2 ** (self.winnum))
                        self.winnum = 0
                        print("money:", round(self.money, 2))
                    else:
                        self.money += item['cj'] * (2 ** (self.winnum))
                        self.winnum += 1
                        print("money:", round(self.money, 2))
                else:
                    self.money -= item['cj'] * (2 ** (self.winnum))
                    self.winnum = 0
                    print("money:", round(self.money, 2))
        print("money:",round(self.money,2))
        print(len(aclist))


Nas().test(aclist)

