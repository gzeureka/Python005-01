#!/usr/bin/env python

# 由 Dijkstra 提出并解决的哲学家就餐问题是典型的同步问题。
# 该问题描述的是五个哲学家共用一张圆桌，分别坐在五张椅子上，在圆桌上有五个盘子和五个叉子，
# 他们的生活方式是交替的进行思考和进餐，思考时不能用餐，用餐时不能思考。
# 平时，一个哲学家进行思考，饥饿时便试图用餐，只有在他同时拿到他的盘子左右两边的两个叉子时才能进餐。进餐完毕后，他会放下叉子继续思考
# 请写出代码来解决如上的哲学家就餐问题，要求代码返回“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录

import threading


class DiningPhilosophers:
    def __init__(self):
        pass

    # philosopher 哲学家的编号。
    # pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
    # eat 表示吃面。
    # putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
    def wantsToEat(self,
                   philosopher,
                   pickLeftFork(),
                   pickRightFork(),
                   eat(),
                   putLeftFork(),
                   putRightFork())


if __name__ == '__main__':
    pass
