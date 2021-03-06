#-*- coding: UTF-8 -*-
#!user/bin/env python
'''
author:zz
time:2017-12-31
version:2.0.2
more:www.zhangshengze.cn
'''
import socket,os,struct,time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST_TX = '139.199.39.95 '.strip() #需要连接的远程IP 公网
HOST = '223.104.17.203 '.strip() #需要连接的远程IP 公网
HOST = '192.168.43.90 '.strip() #需要连接的远程IP 公网

PORT = 50000  #服务器端绑定的端口

s.connect((HOST,PORT))

# 获取本机计算机名称
hostname = socket.gethostname()
# 获取本机ip
ip = socket.gethostbyname(hostname)
print(ip)

print('connection success!')

def conn():
    while 1:
        filePath = str(input("Please Enter Path:"))
        try:
            fo = open(filePath, 'rb')
        except:
            print('Please input the right path.')
            continue
        if os.path.isfile(filePath):
            fileinfo_size =  struct.calcsize('128s1I') # 定义打包规则
            #定义文件头信息，包含文件名和大小
            fhead = struct.pack('128s1I',bytes(os.path.basename(filePath),encoding='utf-8'),os.stat(filePath).st_size)

            s.send(fhead)  # 先发送预信息
            print('Client filePath:',filePath)

            while 1:
                try:
                    filedata = fo.read(1024 * 8)
                except:
                    filedata = fo.read(1024)
                if not filedata:
                    break
                s.send(filedata)
            fo.close()
            print('Ending...')
        else:
            pass
        s.close()

conn()
