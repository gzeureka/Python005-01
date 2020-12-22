#!/usr/bin/env python
#
# 使用 Python+redis 实现高并发的计数器功能
# counter 函数为统计视频播放次数的函数，每调用一次，播放次数 +1
# 参数 video_id 每个视频的 id，全局唯一
# 基于 redis 实现自增操作，确保线程安全

import redis

def counter(client, video_id: int):
    client.incr(video_id)
    
    print(client.get(video_id).decode())
    return client.get(video_id).decode()

def main():
    # 连接 Redis
    client = redis.Redis(host='127.0.0.1', password='do#gLm3nWq')

    # 删除旧数据
    client.delete(1001)
    client.delete(1002)

    counter(client, 1001)
    counter(client, 1001)
    counter(client, 1002)
    counter(client, 1001)
    counter(client, 1002)

if __name__ == '__main__':
    main()
