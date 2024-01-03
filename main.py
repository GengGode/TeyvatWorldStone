# 服务后端，用户接口及数据上传接口
# 用户接口：用户登录
# 数据上传接口：track(float x, float y, float z, float a, float r, float time)
# 上传数据格式：x,y,z,a,r,time
# 数据库：MySQL


from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import pymysql
import time
import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 数据库配置，目前使用本地数据库
db_config = { "host": "localhost", "port": 30000, "user": "root", "password": "root", "database": "test"}
db = pymysql.connect(**db_config)
cursor = db.cursor()

# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    # 获取前端传来的数据
    data = request.get_data()
    data = json.loads(data)
    username = data['username']
    password = data['password']
    # 预处理，防止SQL注入
    username = pymysql.escape_string(username)
    password = pymysql.escape_string(password)
    # 查询数据库
    sql = "SELECT * FROM user WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor.execute(sql)
    result = cursor.fetchall()
    # 返回数据
    if len(result) == 0:
        return jsonify({'code': 0, 'msg': '用户名或密码错误'})
    else:
        return jsonify({'code': 1, 'msg': '登录成功'})

# 数据上传接口
@app.route('/track', methods=['POST'])
def track():
    # 获取前端传来的数据
    data = request.get_data()
    data = json.loads(data)
    x = float(data['x'])
    y = float(data['y'])
    z = float(data['z'])
    a = float(data['a'])
    r = float(data['r'])
    t = datetime(data['time'])
    # 获取当前时间
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    # 插入数据库
    sql = "INSERT INTO track (x, y, z, a, r, time) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (x, y, z, a, r, t))
    db.commit()
    # 返回数据
    return jsonify({'code': 1, 'msg': '上传成功'})

if __name__ == '__main__':
    app.run(host='127.0.0 .1', port=5000, debug=True)
