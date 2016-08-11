# import json
# from redis import Redis
# r = Redis()
# raw = r.get('G4gQX')
# print(raw)
# print(raw.decode(encoding='utf-8'))
# print(json.loads(raw.decode(encoding='utf-8')))

import requests
from redis import Redis
import time 
import json
import config

payload = {'pw': 'cc'}
r = Redis()

while True:
    try:
        response = requests.post(config.url + config.HUIKU_URL, json=payload)
    except Exception as e:
        print (e)
        time.sleep(10)
        continue
    
    try:
        users = response.json()
        users = users['users']
        if users == []:
            continue
        

        for user in users:
            # r.set(user[0], user[1])
            print(user[0], user[1], user[2])
            key = user[0]
            value = user[1:]

            r.set(key, json.dumps(value))
        print(len(users))
        print()
    except Exception as e:
        print('error')
        print (e)
        continue
    
    time.sleep(5)