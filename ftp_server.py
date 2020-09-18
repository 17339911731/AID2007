"""
ftp 文件服务器 服务端
多线程tcp并发模型
"""

from threading import Thread
from socket import *
import sys, os
import time

# 网络地址
HOST = '0.0.0.0'
PORT = 8880
ADDR = (HOST, PORT)

# 文件库位置
FTP = "/home/tarena/FTP/"


# 类用于处理客户端的事件
class FTPServer(Thread):
    def __init__(self, connfd):
        # 客户端链接套接字设置为属性
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        # 判断文件库是否为空
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b'FAIL')
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)  # 防止粘包
            # 使用\n做消息边界,拼接文件列表
            data = '\n'.join(file_list)
            self.connfd.send(data.encode())

    # 处理上传
    def do_stor(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"OK")
            # 接收文件
            file = open(FTP + filename, 'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                file.write(data)
            file.close()

    # 处理下载
    def do_retr(self, filename):
        try:
            file = open(FTP + filename, 'rb')
        except:
            # 文件不存在
            self.connfd.send(b'FAIL')
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
            while True:
                data = file.read(1024 * 10)
                if not data:
                    break
                self.connfd.send(data)
            # 表示文件已经发送结束
            time.sleep(0.1)
            self.connfd.send(b'##')
            file.close()

    # 处理客户端事件
    def run(self):
        # 总分 接收某一个客户端各种请求分情况处理
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == "EXIT":
                break
            elif data == 'LIST':
                self.do_list()
            elif data[:4] == 'STOR':
                # "STOR filename"
                filename = data.split(' ')[-1]
                self.do_stor(filename)
            elif data[:4] == 'RETR':
                # "RETR filename"
                filename = data.split(' ')[-1]
                self.do_retr(filename)

        self.connfd.close()


# 搭建并发网络
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d" % PORT)

    # 循环等待客户端链接
    while True:
        try:
            connfd, addr = sock.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sys.exit("服务结束")

        # 为连接进来的客户端创建新的线程
        t = FTPServer(connfd)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
