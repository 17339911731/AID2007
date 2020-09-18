"""
基于多线程的tcp并发模型

重点代码 !!
"""

from threading import Thread
from socket import *
import sys

# 网络地址
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 类用于处理客户端的事件
class MyThread(Thread):
    def __init__(self,connfd):
        # 客户端链接套接字设置为属性
        self.connfd = connfd
        super().__init__()

    # 处理客户端事件
    def run(self):
        while True:
            data = self.connfd.recv(1024)
            if not data:
                break
            print(data.decode())
            self.connfd.send(b'ok')
        self.connfd.close()

# 搭建并发网络
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d"%PORT)

    # 循环等待客户端链接
    while True:
        try:
            connfd,addr = sock.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sys.exit("服务结束")

        # 为连接进来的客户端创建新的线程
        t = MyThread(connfd)
        t.setDaemon(True)
        t.start()

if __name__ == '__main__':
    main()