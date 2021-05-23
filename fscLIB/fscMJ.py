#! /bin/python3

from threading import Thread
from multiprocessing import Process
from random import randint


def red(l_inp_b:int, x:int=0):
    if x:
        g = ""
        for _ in range(l_inp_b): g += chr(randint(0, 129))
    else:
        g = [chr(randint(0, 129)) for _ in range(l_inp_b)]


def ctl_red():
    global l_inp_b
    while True:
        try:
            t1 = Thread(target=red(l_inp_b, x=1))
            t2 = Thread(target=red(l_inp_b))
            t1.start()
            t2.start()
            t1.join()
        except:
            break

l_inp_b:int = 2 ** 9
def GEN_CTL(l_inp_b_:int=0):
    global l_inp_b
    l_inp_b = l_inp_b_
    ctl_t = Process(target=ctl_red, daemon=True)
    for i in range(2):
        if not i: ctl_t.start()
        if i: ctl_t.terminate()
        yield


if __name__ == "__main__":
    GB = input(" GB > ")
    gen_ctl = GEN_CTL(int(GB) * (10 ** 9))
    next(gen_ctl)
    print(" [*]")
    input(" break [ENTER]>")
    next(gen_ctl)
