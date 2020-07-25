import threading
import time
import hashlib
import requests
import json
import time
import random


class Gogogo(threading.Thread):
    def __init__(self, appId, appKey, whiteUrl, leancloudUrl, urls):
        threading.Thread.__init__(self)
        self.appId = appId
        self.appKey = appKey
        self.whiteUrl = whiteUrl  # 网站白名单
        self.leancloudUrl = leancloudUrl  # leancloud的地址
        self.curlUrls = urls  # 评论地址列表
        self.commentText = ''
        self.commentForm = ''
        self.mails = ['qq', '163', 'outlook', '126', '189', 'foxmail']
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
            "x-lc-ua": "LeanCloud-JS-SDK/3.15.0 (Browser)",
        }
        self.data = {
            "ACL": {"*": {"read": True}},
            "QQAvatar": "https://q2.qlogo.cn/headimg_dl?dst_uin=%s&spec=100" % (random.randint(1000000, 9999999999)),
            "comment": "<p>"+"%s" % (self.commentText)+"</p>",
            "insertedAt": {"__type": "Date", "iso": "2020-0%s-%sT0%s:%s:02.979Z" % (random.randint(0, 9), random.randint(1, 30), random.randint(0, 19), random.randint(0, 60))},
            "ip": "%s.%s.%s.%s" % (random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)),
            "link": self.whiteUrl,
            "mail": "%s@%s.com" % (random.randint(1000000, 9999999999), self.mails[random.randint(0, len(self.mails)-1)]),
            "nick": self.commentForm,
            "ua": "Mozilla/5.0 (Windows NT %s.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.4103.61 Safari/537.36 Edg/%s.0.478.37" % (random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)),
            "url": '/',
            "createdAt": {"__type": "Date", "iso": "2020-0%s-%sT0%s:%s:02.979Z" % (random.randint(0, 9), random.randint(1, 30), random.randint(0, 19), random.randint(0, 60))},
            "updatedAt": {"__type": "Date", "iso": "2020-0%s-%sT0%s:%s:02.979Z" % (random.randint(0, 9), random.randint(1, 30), random.randint(0, 19), random.randint(0, 60))}
        }
        # 2020-01-22T02:25:02.979Z
    # MD5加密

    def my_md5(self, s):
        m = hashlib.md5(s.encode())
        return m.hexdigest()  # 获取加密后的字符串

    # 得到评论的地址

    def getCurl(self):
        num = random.randint(0, len(self.curlUrls) - 1)
        print(self.curlUrls[num])
        return self.curlUrls[num]

    # 设置评论的内容与评论地址

    def getCommentText(self):
        try:
            obj = json.loads(requests.get(
                'https://international.v1.hitokoto.cn/').text)
        except:
            obj = False
        time = {"__type": "Date", "iso": "2020-0%s-%sT0%s:%s:02.979Z" % (random.randint(
            0, 9), random.randint(0, 100), random.randint(0, 100), random.randint(0, 60))}

        self.data = {
            "ACL": {"*": {"read": True}},
            "QQAvatar": "https://q2.qlogo.cn/headimg_dl?dst_uin=%s&spec=100" % (random.randint(1000000, 9999999999)),
            "comment": "<p>"+"%s" % (self.commentText)+"</p>",
            "insertedAt": time,
            "ip": "%s.%s.%s.%s" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "link": self.whiteUrl,
            "mail": "%s@%s.com" % (random.randint(1000000, 9999999999), self.mails[random.randint(0, len(self.mails)-1)]),
            "nick": self.commentForm,
            "ua": "Mozilla/5.0 (Windows NT %s.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.4103.61 Safari/537.36 Edg/%s.0.478.37" % (random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)),
            "url": self.getCurl(),
            "createdAt": time,
            "updatedAt": time
        }
        if (obj):
            self.data['comment'] = "<p>" + obj['hitokoto'] + "</p>"
            self.data['nick'] = obj['from']
            return "%s-------%s" % (self.data['comment'], self.data['nick'])
        else:
            self.data['comment'] = "大佬太强了！！！"
            self.data['nick'] = '一个菜鸟！！！'
            return "%s-------%s" % ("大佬太强了！！！", "一个菜鸟！！！")

    def run(self):
        while True:
            self.getCommentText()
            r = requests.post(self.leancloudUrl,
                              headers=self.headers, data=json.dumps(self.data))
            print(r.text)
# return r


# 评论页面的列表 支持多个
# urls = ['/messageboard/', "/10007/06/07/hello%20word/", "/2020/07/15/github%E9%A1%B9%E7%9B%AE/", "/2020/07/15/github%E9%A1%B9%E7%9B%AE/", "/2020/07/13/deepin/", "/2020/07/13/deepin/","/2020/07/07/my-qqmusic-mv/", "/2020/07/07/my-qqmusic-mv/", "/2020/06/29/butterfly%E4%BC%98%E5%8C%96/", "/2020/06/29/butterfly%E4%BC%98%E5%8C%96/", "/2020/06/26/Linux%20basic/"]
# range参数为线程参数
urls = ["/archives/cbcd1946.html", "/archives/b3aa6458.html", "/archives/353666f0.html", "/archives/292a04a3.html", "/archives/14862ea.html", "/archives/d343d10e.html", "/archives/838e5b66.html", "/archives/ad48558a.html", "/archives/c9ba00d6.html", "/archives/c53925ef.html", "/archives/238bcadf.html", "/archives/e8e03d57.html", "/archives/8eb7b9b8.html", "/archives/354a6d83.html", "/archives/5cca81b.html", "/archives/87dc25e4.html", "/archives/f36eea83.html", "/archives/2798a2b1.html", "/archives/f06684a1.html", "/archives/f09f3fc0.html", "/archives/b1e33f9d.html", "/archives/88be941b.html", "/archives/285695a6.html", "/archives/54c51cfa.html", "/archives/e358bc47.html", "/archives/cc0b1d61.html", "/archives/2f89d13b.html", "/archives/ce7a0d96.html", "/archives/92c1fbae.html", "/archives/5b20fbd0.html", "/archives/9898af63.html", "/archives/15049ec0.html", "/archives/f93d436.html", "/archives/56903ee1.html", "/archives/995b88f0.html", "/archives/6fd4fff1.html", "/archives/dde01238.html", "/archives/d18fd292.html", "/archives/fde43a3f.html", "/archives/868f84ed.html", "/archives/9013c8d8.html", "/archives/e8460ade.html", "/archives/e3dc5cbb.html", "/archives/540169c9.html", "/archives/264a3045.html", "/archives/a2423b27.html", "/archives/477f8de2.html", "/archives/258df3be.html", "/archives/c739ddf8.html", "/archives/4bfa5187.html",
        "/archives/5b5154c.html", "/archives/57b9b1ea.html", "/archives/e21c4730.html", "/archives/c08bb6f8.html", "/archives/26f3bff6.html", "/archives/7e878b19.html", "/archives/f36d08b9.html", "/archives/b07ae32c.html", "/archives/8737131e.html", "/archives/1567847a.html", "/archives/1212afb3.html", "/archives/a0f8eb24.html", "/archives/44b2b83c.html", "/archives/44b2b83c.html", "/archives/3b45b587.html", "/archives/741e0ba.html", "/archives/8c9422d9.html", "/archives/a26302a1.html", "/archives/46f06641.html", "/archives/ae8398fc.html", "/archives/f5f1da44.html", "/archives/19fc55fb.html", "/archives/b2cd753e.html", "/archives/16f8f18e.html", "/archives/a31746e9.html", "/archives/ad512fcf.html", "/archives/2c25c1c9.html", "/archives/802ec22c.html", "/archives/1c5148b1.html", "/archives/Infinity.html", "/archives/3babbc01.html", "/archives/332d35b.html", "/archives/f78977b6.html", "/archives/e6b31439.html", "/archives/c69cf5a7.html", "/archives/41e021ef.html", "/archives/4f1f2f20.html", "/archives/628e35f6.html", "/archives/9da3e761.html", "/archives/199f7244.html", "/archives/cc98362f.html", "/archives/84c3a399.html", "/archives/9e1390b6.html", "/archives/822245c.html", "/archives/df21d8f8.html", "/archives/344c0f13.html", "/archives/738bac5d.html", "/archives/56cec031.html", "/archives/25109d5c.html", "/archives/c4bd2243.html"]
# range参数为线程参数
for i in range(1):
    # 第一个参数表示appKey,第二个参数表示appId，第三个参数表示允许评论的白名单（通常为博客域名），第四个参数表示leancloud的地址，第五个参数表示需要刷取的页面列表
    leteNB = Gogogo('pNpXnDYbw5Rv8Dqbhxyp5sWv', 'nt4vcGCJQrkz0tDPth9dzD6W-gzGzoHsz',
                    'https://blog.juanertu.com', 'https://avoscloud.com/1.1/classes/Comment', urls)
    leteNB.start()
