#!/usr/bin/env python
# 不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能
# 本文件是服务端代码
#
# 改进：可以对 Client 和 Server 的通讯协议进行增强，例如 Client 将文件名送给 Server；对传输的数据进行校验和检查等。

import socket

HOST = 'localhost'
PORT = 10000

BLOCK_SIZE = 1024
SAVE_FILE_NAME = 'test.saved'


def file_server():
    '''File Transfer 的 Server 端'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    s.bind((HOST, PORT))
    # 监听客户端连接请求，只接受一个连接
    s.listen(1)
    print(f'Server is listening on port {PORT}')

    while True:
        # 接受客户端连接
        conn, addr = s.accept()
        # 输出客户端地址
        print(f'Connected by {addr}')

        with open(SAVE_FILE_NAME, mode='wb') as f:
            while True:
                # 接收数据
                data = conn.recv(BLOCK_SIZE)
                if not data:
                    break
                # 写入文件
                print(f'Received {len(data)} bytes')
                f.write(data)
            
            print(f'Save to "{SAVE_FILE_NAME}"')

        # 关闭连接
        conn.close()
        print(f'Disconnected {addr}')

    s.close()


if __name__ == '__main__':
    file_server()
