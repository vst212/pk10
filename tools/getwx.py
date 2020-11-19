
import json
# 这个地方必须这么写 函数名：response
def response(flow):
    # 通过抓包软包软件获取请求的接口
    print("抓...")
    if 'mp.weixin.qq.com' in flow.request.url:
        # 数据的解析
        print("抓到了")