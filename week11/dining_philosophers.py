#!/usr/bin/env python

# 由 Dijkstra 提出并解决的哲学家就餐问题是典型的同步问题。
# 该问题描述的是五个哲学家共用一张圆桌，分别坐在五张椅子上，在圆桌上有五个盘子和五个叉子，
# 他们的生活方式是交替的进行思考和进餐，思考时不能用餐，用餐时不能思考。
# 平时，一个哲学家进行思考，饥饿时便试图用餐，只有在他同时拿到他的盘子左右两边的两个叉子时才能进餐。进餐完毕后，他会放下叉子继续思考
# 请写出代码来解决如上的哲学家就餐问题，要求代码返回“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录
#
# 测试用例：
#
# 输入：n = 1 （1<=n<=60，n 表示每个哲学家需要进餐的次数。）
# 预期输出：
#
# [[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
# 解释:
#
# 输出列表中的每一个子列表描述了某个哲学家的具体行为，它的格式如下：
# output[i] = [a, b, c] (3 个整数)
#
# a 哲学家编号。
# b 指定叉子：{1 : 左边, 2 : 右边}.
# c 指定行为：{1 : 拿起, 2 : 放下, 3 : 吃面}。
# 如 [4,2,1] 表示 4 号哲学家拿起了右边的叉子。所有自列表组合起来，就完整描述了“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录。

import sys
import threading

PICK_LEFT_FORK = [1, 1]
PICK_RIGHT_FORK = [2, 1]
EAT = [0, 3]
PUT_LEFT_FORK = [1, 2]
PUT_RIGHT_FORK = [2, 2]


class DiningPhilosopher(threading.Thread):
    # num 哲学家的编号
    # eat_times 需要进餐的次数
    def __init__(self, num, eat_times):
        super().__init__()
        self.num = num
        self.eat_times = eat_times

    def pickLeftFork(self):
        print([self.num] + PICK_LEFT_FORK)

    def pickRightFork(self):
        print([self.num] + PICK_RIGHT_FORK)

    def eat(self):
        print([self.num] + EAT)

    def putLeftFork(self):
        print([self.num] + PUT_LEFT_FORK)

    def putRightFork(self):
        print([self.num] + PUT_RIGHT_FORK)

    # pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
    # eat 表示吃面。
    # putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
    def wantsToEat(self):
        # 0号哲学家拿叉子的顺序与其他人相反
        if self.num == 0:
            self.pickLeftFork()
            self.pickRightFork()
            self.eat()
            self.putLeftFork()
            self.putRightFork()
        else:
            self.pickRightFork()
            self.pickLeftFork()
            self.eat()
            self.putRightFork()
            self.putLeftFork()

    def run(self):
        for _ in range(self.eat_times):
            self.wantsToEat()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('请输入需要进餐的次数')
        exit(1)

    eat_times = int(sys.argv[1])
    for i in range(5):
        p = DiningPhilosopher(i, eat_times)
        p.start()
