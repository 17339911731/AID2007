"""
创建两个线程,同时执行
一个线程打印 A---Z
一个线程打印 1--52
要求打印顺序为 12A34B56C...5152Z

提示: 使用同步互斥方法
"""
from threading import Thread,Lock

lock1 = Lock()
lock2 = Lock()

def print_num():
    for i in range(1,53,2):
        lock1.acquire()
        print(i)
        print(i + 1)
        lock2.release()

def print_chr():
    for i in range(65,91):
        lock2.acquire()
        print(chr(i))
        lock1.release()


t1 = Thread(target = print_num)
t2 = Thread(target = print_chr)

lock2.acquire() # 先打印数字,所以字母线程先锁住

t1.start()
t2.start()
t1.join()
t2.join()