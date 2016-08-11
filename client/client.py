from gevent import monkey
monkey.patch_all()

import gevent
from gevent.pool import Group
from gevent.queue import Queue, Empty
import requests
import download
import json
import time
import config


CONTROLLER = config.url + config.INDEX_URL #'http://127.0.0.1:5000/lmiguelvargasf/'
CONTROLLER_POST = config.url + config.XUYAO_URL #'http://127.0.0.1:5000/lmiguelvargasf/xuyao/'

tasks = Queue()
group = Group()
users = []

def crawler():
    global users
    while True:
        try:
            url = tasks.get(timeout=1)
            result = download.download_user(url)
        except Empty:
            break
        if result != None:
            users.append(result)

asn = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def generate_url(i):
    if i>62*62*62:
        return False
    i = i-1
    ch1 = asn[i%62]
    ch2 = asn[i/62%62]
    ch3 = asn[i/62/62%62]
    ch4 = asn[i/62/62/62%62]
    
    for index,ch in enumerate(asn):
        url = 'http://www.zhihu.com/l/' + 'G' +ch3+ch2+ch1+ch
        # url = 'http://www.zhihu.com/l/G4gQ' + ch  
        tasks.put(url)

    return True


while True:
    payload = {'pw': 'cc'}
    try:
        r = requests.post(CONTROLLER, json=payload)
    except:
        time.sleep(5)
        print 'error'
        continue
    print r.text

    # stop the crawler
    if generate_url(int(r.text)) == False:
        break
    
    # clean users list
    users = []
    for i in range(4):
        g = gevent.spawn(crawler)
        group.add(g)

    group.join()

    if users == []:
        payload = {'empty': 'yes'}
    else:
        payload = {'users': users}
    
    r = requests.post(CONTROLLER_POST, json=payload)

    if users == []:
        print payload
    print r.text


    time.sleep(5)
    # break