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
urls = ["/p/314.html", "/p/312.html", "/p/310.html", "/p/309.html", "/p/308.html", "/p/305.html", "/p/304.html", "/p/303.html", "/p/297.html", "/p/291.html", "/p/290.html", "/p/289.html",
        "/p/279.html", "/p/276.html", "/p/169.html", "/p/144.html", "/p/142.html", "/p/113.html", "/p/109.html", "/p/90.html", "/p/67.html", "/p/37.html", "/p/20.html", "/p/13.html", "/p/1.html"]
# range参数为线程参数
for i in range(100):
    # 第一个参数表示appKey,第二个参数表示appId，第三个参数表示允许评论的白名单（通常为博客域名），第四个参数表示leancloud的地址，第五个参数表示需要刷取的页面列表
    leteNB = Gogogo('VqWNlK7hzx1WqjdzDyPxsacY', 'TdVKlegqiv6xKhX1avnspp6g-gzGzoHsz',
                    'https://ifking.cn', 'https://tdvklegq.api.lncld.net/1.1/classes/Comment', urls)
    leteNB.start()
