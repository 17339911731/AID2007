"""
ftp 文件服务器 客户端
"""
from socket import *
from time import sleep
import sys

# 服务端地址
ADDR = ('127.0.0.1', 8880)


# 具体与服务端进行交互的类
class FTPClient:
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):
        self.sock.send(b'LIST')
        # 等待回复
        result = self.sock.recv(128).decode()
        # 根据回复分情况应对
        if result == 'OK':
            # 接收文件列表
            files = self.sock.recv(1024 * 1024)
            print(files.decode())
        else:
            print("文件库为空")

    # 上传文件
    def do_stor(self, filename):
        # 本地判断文件是否存在
        try:
            file = open(filename, 'rb')
        except:
            print("文件不存在")
            return

        # 提取文件名
        filename = filename.split('/')[-1]
        # 发送请求
        msg = "STOR " + filename
        self.sock.send(msg.encode())
        # 等待反馈
        result = self.sock.recv(128).decode()
        # 分情况讨论
        if result == 'OK':
            while True:
                data = file.read(1024 * 10)
                if not data:
                    break
                self.sock.send(data)
            # 表示文件已经发送结束
            sleep(0.1)
            self.sock.send(b'##')
            file.close()
        else:
            print("文件已存在")

    # 下载文件
    def do_retr(self, filename):
        # 发送请求
        msg = "RETR " + filename
        self.sock.send(msg.encode())
        # 等待回复
        result = self.sock.recv(128).decode()
        if result == 'OK':
            file = open(filename, 'wb')
            while True:
                data = self.sock.recv(1024)
                if data == b'##':
                    break
                file.write(data)
            file.close()
        else:
            print("文件不存在")

    # 退出
    def do_exit(self):
        self.sock.send(b'EXIT')
        self.sock.close()
        sys.exit("谢谢使用")


def main():
    # 链接服务器
    sock = socket()
    sock.connect(ADDR)

    # 实例化对象,用于调用类中的具体方法发起请求
    ftp = FTPClient(sock)

    while True:
        print("\n====== 命令选项 ======")
        print("***     list         ***")
        print("***   stor filename  ***")
        print("***   retr filename  ***")
        print("***     exit         ***")
        print("========================")

        cmd = input("请输入命令:")
        if cmd == "list":
            ftp.do_list()
        elif cmd[:4] == "stor":
            # 提取文件名
            filename = cmd.split(' ')[-1]
            ftp.do_stor(filename)
        elif cmd[:4] == "retr":
            # 提取文件名
            filename = cmd.split(' ')[-1]
            ftp.do_retr(filename)
        elif cmd == 'exit':
            ftp.do_exit()
        else:
            print("请输入正确指令")


if __name__ == '__main__':
    main()
