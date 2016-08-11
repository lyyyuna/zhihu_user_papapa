from flask import Flask, request
from redis import Redis
import json
import config

app = Flask(__name__)
r = Redis()

@app.route(config.INDEX_URL, methods=['POST'])
def index():
    data = request.json
    if data.get('pw') == config.PASSWORD:
        c = r.incr('user_count')
    else:
        return 'N'
    return str(c)

@app.route(config.XUYAO_URL, methods=['POST'])
def xuyao():
    data = request.json
    if data.get('empty') == 'yes':
        pass
    elif data.get('users') != None: 
        users = data.get('users')
        print (len(users))
        for user in users:
            key = user[0]
            value = user[1:]
            r.set(key, json.dumps(value))

    c = r.incr('finish_count')
    return str(c)

@app.route(config.HUIKU_URL, methods=['POST'])
def huiku():
    data = request.json
    if data.get('pw') == config.PASSWORD:
        keys = {}
        users = []
        for i in range(0, 100):
            key = r.randomkey()
            keys[key] = 1
        for key, value in keys.items():
            key = key.decode('ascii')
            if key == 'user_count' or key == 'finish_count':
                continue
            userinfo = r.get(key)
            userinfo = json.loads(userinfo.decode(encoding='utf-8'), encoding='utf-8')
            r.delete(key)
            users.append([key]+ userinfo)
        payload = {'users' : users}
        return json.dumps(payload)
            
    else:
        return '0'

if __name__ == '__main__':
    app.run(debug=True)