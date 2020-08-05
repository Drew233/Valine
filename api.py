import threading
import time
import hashlib
import requests
import json
import time
import random


class Gogogo(threading.Thread):
    def __init__(self, appId, appKey, whiteUrl, leancloudUrl):
        threading.Thread.__init__(self)
        self.appId = appId
        self.appKey = appKey
        self.whiteUrl = whiteUrl  # 网站白名单
        self.leancloudUrl = leancloudUrl  # leancloud的地址
        self.nowTime = str(int(time.time() * 1000))
        self.headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "charset": "UTF-8",
            "origin": self.whiteUrl,
            "referer": self.whiteUrl,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64",
            "x-lc-id": self.appKey,
            "x-lc-sign": "%s,%s" % (self.my_md5(self.nowTime+self.appId), self.nowTime),
            "x-lc-ua": "LeanCloud-JS-SDK/4.6.0 (Browser)",
        }
        self.data = {
            "password": "1",
            "username": "1·"
        }
    # MD5加密

    def my_md5(self, s):
        m = hashlib.md5(s.encode())
        return m.hexdigest()  # 获取加密后的字符串

    def run(self):
        while True:
            r = requests.get(self.leancloudUrl,
                             headers=self.headers, data=json.dumps(self.data))
            print(r.text)
# return r


# range参数为线程参数
for i in range(100):
    # 第一个参数表示appKey,第二个参数表示appId，第三个参数表示允许评论的白名单（通常为博客域名），第四个参数表示leancloud的地址，第五个参数表示需要刷取的页面列表
    leteNB = Gogogo('bUG2OW4oaVi3OKPNiPxGDy8o', 'v7RUELXqRXpxactiQlFOa7st-MdYXbMMI',
                    'https://cndrew.cn/', 'https://v7ruelxq.api.lncldglobal.com/1.1/classes/shuoshuo?where=%7B%7D&limit=5&order=-createdAt')
    leteNB.start()
