#!/usr/bin/env python
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
import time


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        print(f'total {time.time() - start_time}')
        return ret
    return inner


@timer
def foo(n):
    time.sleep(n)


if __name__ == '__main__':
    # sleep 1.5
    foo(1.5)
