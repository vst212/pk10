import datetime
import json
import time
import urllib
from urllib.parse import quote



import gitlab
import requests

client = gitlab.Gitlab("https://gitlab.dottmed.com/", private_token='sumzgzzHqUfysgJ_wqg9', timeout=2)
client.auth()

project = client.projects.get('liaofeng/lddb_server')
commits = project.commits.list(ref_name='dev', page=0, per_page=50)

username ="jack"

def getmycommits():
    mycommit = []
    for c in commits:
        created_at = datetime.datetime.strptime(c.created_at, "%Y-%m-%dT%H:%M:%S.000+08:00")
        if c.committer_name == username:
            if "Merge" in c.message:
                pass
            elif created_at.date() == datetime.datetime.now().date():
                mycommit.append(c.message)
    mycommit =list(set(mycommit))
    return  mycommit


def create_journal(mycommit):
    url="https://app.work.weixin.qq.com/wework_admin/journal/api/create_journal"

    post_time = int(time.time()*1000)
    current = int(time.time())
    print(time.time())

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1305.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 wxwork/3.0.36 (MicroMessenger/6.2) WindowsWechat",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN",
        "Referer": "https://app.work.weixin.qq.com/wework_admin/journal/desktop/create?tempid=Bs2iyL4hzwTntcaf4uUAe6bgwgAEunUDbx8c3HE3p&vid=1688853437968789&corpid=1970325096073303&event_type=40000001&termid=65537&host_vid=1688853437968789",
        "Cookie": "wwrtx.c_gdpr=0; pgv_pvid=2873445283; wwapp.vid=1688853437968789; wwapp.st=27DBDBE3727FB02485F4D62B0F73E54176D1D553520F2270A84BBEDA61DAD28B6A9C7562C9C3450FC9808B02EF9A80169BE6620B61F47CC4AF2A41BCF3A273C2F8C2123697963724EC4B5B8D9F1688F827D6AD7775B0ECB73D9086BE6C388AB5777D59480AFFCDE7705150FD6F7D76D422206C37C7622EFD759D5FF1A5D5A6C986EBA2BEF3B303BE484A7806CD9EC797; wwapp.cst=09C49B6DFC9CDCB5C8BDD6DC05E305C3682D5110871BD93D7EEEF3BEEDDC3A07ABCADFC735A0E335B0297444705BCDE7; wwapp.deviceid=018230d2-114f-4eab-a5fb-e43579a6f623; ww_rtkey=8ck0eqb; wwapp.h5_worknote.skey=DBn8dP8JNvw10sAaI6W6cmWlvNTqM4GuicNmeSXrUZZoQSR19CPl6Bp3q9DF_plHg7eCVEAyMwokpTHnBb2C6w; wwapp.vid=1688853437968789; wwrtx.i18n_lan=zh",
        "Accept-Encoding": "gzip, deflate"
    }

    mycommit = " ".join(mycommit)
    appdata= {"contents":[{"id":"Date-"+str(post_time),"control":"Date","title":[{"text":"日报日期","lang":"zh_CN"}],"value":{"date":{"type":"day","timestamp":current,"s_timestamp":current}}},{"id":"item-1522054774002","control":"Textarea","title":[{"text":"今日工作","lang":"zh_CN"}],"value":{"text":mycommit}},{"id":"item-1522054819891","control":"Textarea","title":[{"text":"明日计划","lang":"zh_CN"}],"value":{"text":""}},{"id":"item-1522054838712","control":"Textarea","title":[{"text":"其他事项","lang":"zh_CN"}],"value":{"text":""}},{"id":"item-1522237984497","control":"File","title":[{"text":"附件","lang":"zh_CN"}],"value":{"files":[]}}]}

    appstr = json.dumps(appdata,ensure_ascii=False) + '&event_type=40000001&template_id=Bs2iyL4hzwTntcaf4uUAe6bgwgAEunUDbx8c3HE3p&template_name_lang=[{"text":"日报","lang":"zh_CN"}]&reporter[0][vid]=%s&journal_id=0&termid=65537&roomlist=[]}'% post_time


    data={"apply_data":urllib.parse.quote(appstr.encode('utf-8'))}
    print(urllib.parse.quote(appstr.encode('utf-8')))
    res= requests.post(url=url,data=data,headers=headers).json()

    print(res)



def run():
    mycommits= getmycommits()
    print(" ".join(mycommits))

run()
