from __future__ import print_function
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
import random



CONTROLLER = config.url + config.INDEX_URL #'http://127.0.0.1:5000/lmiguelvargasf/'
CONTROLLER_POST = config.url + config.XUYAO_URL #'http://127.0.0.1:5000/lmiguelvargasf/xuyao/'

tasks = Queue()
group = Group()
users = []


print('begin download')

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
        gevent.sleep(config.WORKER_DELAY)

asn = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def generate_url(i):
    if i>62*62*62:
        return False
    i = i-1
    ch1 = asn[i%62]
    ch2 = asn[i//62%62]
    ch3 = asn[i//62//62%62]
    ch4 = asn[i//62//62//62%62]
    
    for index,ch in enumerate(asn):
        url = 'http://www.zhihu.com/l/' + 'G' +ch3+ch2+ch1+ch
        # url = 'http://www.zhihu.com/l/G4gQ' + ch  
        tasks.put(url)

    return True


while True:
    payload = {'pw': 'cc'}
    try:
        r = requests.post(CONTROLLER, json=payload)
        # stop the crawler
        if generate_url(int(r.text)) == False:
            break
    except Exception as e:
        print ('controller no response error')
        print (e)
        time.sleep(config.CLIENT_CONTROLLER_NO_RESPONSE_DELAY)
        continue
    print ('user_count: ', r.text)


    
    # clean users list
    users = []
    for i in range(config.WORKER_NUM):
        g = gevent.spawn(crawler)
        group.add(g)

    group.join()

    if users == []:
        payload = {'empty': 'yes'}
    else:
        payload = {'users': users}
    
    while True:
        flag = False
        try:
            r = requests.post(CONTROLLER_POST, json=payload)
            finish_count = int(r.text)
            flag = True
        except Exception as e:
            print (e)
            print ('controller no response error')

        if flag == True:
            break
        else:
            time.sleep(config.CLIENT_CONTROLLER_NO_RESPONSE_DELAY)
            continue

    if users == []:
        print (payload)
    print ('finish_count: ', r.text)

    rannum = random.random()
    if rannum > 0.9:
        time.sleep(config.CLIENT_LONG_DELAY)
    else:
        time.sleep(config.CLIENT_SHORT_DELAY)
    # break