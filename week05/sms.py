#!/usr/bin/env python
# 在使用短信群发业务时，公司的短信接口限制接收短信的手机号，
# 每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口

import sys
import time
import redis


def can_send(list, limit: int):
    # 未超过 limit 次，可以发送
    if len(list) < limit:
        return True

    # 获取倒数第 limit 次的发送时间
    t = float(list[-limit].decode())
    now = time.time()
    # 时间差是否小于 1 分钟
    if now - t < 60:
        return False
    else:
        return True


def sendsms(client, telephone_number: str, contents: str, key=None):
    # 用 Redis 列表记录每个手机号的最后 5 次发送时间
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    limit = 5
    list = client.lrange(telephone_number, 0, -1)
    if can_send(list, limit):
        # 本次发送的时间加到时间列表末尾
        client.rpush(telephone_number, time.time())
        # 发送时间列表表头出队，减少存储空间
        if len(list) >= limit-1:
            client.ltrim(telephone_number, -limit, -1)
        print("发送成功", telephone_number, contents)
    else:
        print(telephone_number, "1 分钟内发送次数超过 5 次, 请等待 1 分钟")


def main(telephone_number: str):
    # 连接 Redis
    client = redis.Redis(host='127.0.0.1', password='do#gLm3nWq')

    try:
        while True:
            sendsms(client, telephone_number, 'Hello world!')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')


if __name__ == '__main__':
    # 检查命令行参数个数
    if len(sys.argv) < 2:
        print('Please specify a phone number')
        exit(1)

    telephone_number = sys.argv[1]
    main(telephone_number)
