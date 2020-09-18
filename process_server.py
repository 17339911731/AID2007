"""
基于多进程的tcp网络并发模型
    创建网络套接字用于接收客户端请求
    等待客户端连接
    客户端连接，则创建新的进程具体处理客户端请求
    主进程继续等待其他客户端连接
    如果客户端退出，则销毁对应的进程

重点代码 !!!
"""
from multiprocessing import Process
from socket import *
from signal import *
import sys

# 网络地址
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 处理客户端事件
def handle(connfd):
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())
        connfd.send(b'ok')
    connfd.close()

# 搭建并发网络
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d"%PORT)
    signal(SIGCHLD,SIG_IGN) # 处理僵尸进程

    # 循环等待客户端链接
    while True:
        try:
            connfd,addr = sock.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sys.exit("服务结束")

        # 为连接进来的客户端创建新的进程
        p = Process(target=handle,args=(connfd,))
        p.daemon = True # 子进程随父进程退出
        p.start()

if __name__ == '__main__':
    main()





