#!/usr/bin/env python
# 不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能
# 本文件是客户端代码

import socket
import sys
import os

HOST = 'localhost'
PORT = 10000

BLOCK_SIZE = 1024


def file_client(file_name):
    '''File Transfer 的 Client 端'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print(f'Start transfering "{file_name}"')
    with open(file_name, mode='rb') as f:
        # 读取文件
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            # 发送数据
            s.sendall(buf)
            print(f'Sent {len(buf)} bytes')
            buf = f.read(BLOCK_SIZE)

    # 关闭连接
    s.close()
    print(f'File transfer completed')


if __name__ == '__main__':
    # 检查命令行参数个数
    if len(sys.argv) < 2:
        print('Please specify a file to transfer')
        exit(1)

    # 检查文件是否存在
    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print(f'File "{file_name}" does not exist')
        exit(1)

    # 检查指定的是否为文件
    if not os.path.isfile(file_name):
        print(f'"{file_name}" is not a file')
        exit(1)

    file_client(file_name)
