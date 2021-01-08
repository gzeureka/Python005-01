#!/usr/bin/env python
# 自定义一个 python 函数，实现 map() 函数的功能

def my_map(func, *iterables):
    iters = [iter(seq) for seq in iterables]
    while True:
        try:
            yield func(*[next(it) for it in iters])
        except StopIteration:
            return


def add(*numbers):
    return sum(numbers)


def print_result(iterator):
    for i in iterator:
        print(i)


if __name__ == '__main__':
    print_result(my_map(add, [1, 2, 3, 4]))
    print_result(my_map(add, [1, 2, 3, 4], [
                 10, 20, 30, 40], [100, 200, 300, 400]))
