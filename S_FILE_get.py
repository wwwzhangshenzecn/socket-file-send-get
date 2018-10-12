# -*- coding:utf-8 -*-
'''
author:zz
time:2017-12-31
version:2.0.2
more:ww.zhangshengze.cn
'''
import socket,os,struct,time,socketserver

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = '' # 允许通过的链接的IP
PORT = 50000 # 指定端口
ADDR = (HOST,PORT)

# 获取本机计算机名称
hostname = socket.gethostname()
# 获取本机ip
ip = socket.gethostbyname(hostname)
print(ip)

class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):

        print('Waiting...')
        print('connect from :',self.client_address)
        i=0
        while 1:

            fileinfo_size = struct.calcsize('128s1I') #定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            self.buf = self.request.recv(fileinfo_size)

            st = time.time()

            if self.buf :#如果不加这个if，第一个文件传输完成后会自动走到下一句
                self.filename,self.filesize = struct.unpack('128s1I',self.buf) #根据128sl解包文件信息，与client端的打包规则相同
                self.filename = str(self.filename,encoding='utf-8').strip('\00')

                print('filename is:'+self.filename)
                print('file size is :',self.filesize)
                self.filename = os.path.join(('new_'+self.filename).strip('\00'))#使用strip()删除打包时附加的多余空字符
                print(self.filename,type(self.filename)) # 输出文件名 以及 类型

                recved_size = 0 #定义已接受文件的大小
                file = open(self.filename,'wb') #写入方式打开文件，准备写入
                print('Start receving...')
                while not recved_size == self.filesize:
                    if self.filesize - recved_size > 1024*8:
                        rdata = self.request.recv(1024*8)
                        recved_size += len(rdata)
                        if i % 100 == 0:
                            print(i)
                    else:
                        rdata = self.request.recv(self.filesize - recved_size)
                        recved_size = self.filesize

                        print('---',i)
                    file.write(rdata)
                    i += 1
                file.close()
                et = time.time()
                receive_speed = self.filesize / 1024.0 / et
                print("Ending...,the time:",time.time()-st)
                print('the speed: {speed} per KB'.format(speed=receive_speed))

try:
    print('Waiting...')

    tcpServ = socketserver.ThreadingTCPServer(ADDR,MyRequestHandler)
    tcpServ.serve_forever()
except:
    print('连接中断')


