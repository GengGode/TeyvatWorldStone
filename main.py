# 服务后端，用户接口及数据上传接口
# 用户接口：用户登录
# 数据上传接口：track(float x, float y, float z, float a, float r, float time)
# 上传数据格式：x,y,z,a,r,time
# 数据库：MySQL
import datetime
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pymysql

import os
import sys

class track_info(BaseModel):
    x: float
    y: float
    z: float
    a: float
    r: float
    time: datetime.datetime

root_path = os.getcwd()
sys.path.append(root_path)

app = FastAPI()

# 数据库配置，目前使用本地数据库
db_config = { "host": "localhost", "port": 3306, "user": "test", "password": "test123456", "database": "test"}
db = pymysql.connect(**db_config)
cursor = db.cursor()
# 创建表
cursor.execute("DROP TABLE IF EXISTS user")
cursor.execute("DROP TABLE IF EXISTS track")
cursor.execute("CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
cursor.execute("CREATE TABLE track (id INT AUTO_INCREMENT PRIMARY KEY, x FLOAT, y FLOAT, z FLOAT, a FLOAT, r FLOAT, time DATETIME)")


# 用户登录接口
@app.post('/login')
def login():
    '''
    用户登录接口
    :param username: str, 用户名
    :param password: str, 密码
    :return: json, {'code': 1, 'msg': '登录成功'}
    '''

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
        return {'code': 0, 'msg': '用户名或密码错误'}
    else:
        return {'code': 1, 'msg': '登录成功'}


# 数据上传接口
@app.post('/track/')
def track(info: track_info):
    '''
    数据上传接口
    :param info: track_info, 数据信息
    :return: json, {'code': 1, 'msg': '上传成功'}
    '''
    x = info.x
    y = info.y
    z = info.z
    a = info.a
    r = info.r
    time = info.time
    print(x, y, z, a, r, time)
    # 插入数据库
    sql = "INSERT INTO track (x, y, z, a, r, time) VALUES (%s, %s, %s, %s, %s, '%s')" % (x, y, z, a, r, time)
    r = cursor.execute(sql)
    if r == 0:
        return {'code': 0, 'msg': '上传失败'}
    db.commit()
    # 返回数据
    return {'code': 1, 'msg': '上传成功'}
  

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)

