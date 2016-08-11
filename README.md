# zhihu_user_papapa
爬取知乎用户个人资料及关注关系

## 配置

新建一个 config.py

    PASSWORD = ''
    INDEX_URL = '/lmiguelvargasf/'
    XUYAO_URL = '/lmiguelvargasf/xuyao/'
    HUIKU_URL = '/asdfhi12uernifoervn/'

    url = 'http://xxxxxxxxxx'

    WORKER_NUM = 2
    WORKER_DELAY = 2
    CLIENT_LONG_DELAY = 10
    CLIENT_SHORT_DELAY = 20
    DOWNLOAD_TOOFAST_DELAY = 600 # do not edit
    DOWNLOAD_ERROR_DELAY = 100 # do not edit

    CLIENT_CONTROLLER_NO_RESPONSE_DELAY = 5



## Changelog

### 2016.8.11

这是第一版的结构，三角色之间通过 HTTP 协议通信。分成三个角色的原因是，1.分布式提高下载速度，2.虚拟主机内存和硬盘都比较贵，所以搞了个 storedata 存到本地。

- server 是一个 HTTP 服务器，负责分发任务和接收爬取的用户信息。
- client 是一个 gevent 爬虫客户端，从 server 获取编号后开始爬页面并返回用户信息。
- storedata 从 server 中拉取爬完的数据。
