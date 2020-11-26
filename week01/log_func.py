# 编写一个函数, 当函数被调用时，将调用的时间记录在日志中
# 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log
import logging
import time
import os


def log_func():
    logging.info('log_func called %s' % time.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    # 创建保存日志文件的目录
    dir = '/var/log/python-%s' % time.strftime("%Y-%m-%d")
    os.makedirs(dir, exist_ok=True)
    filename = '%s/week01.log' % dir
    print('Loggin information will be written into', filename)

    # 设定保存日志的文件名称，日志级别
    logging.basicConfig(level=logging.INFO, filename=filename)
    while True:
        log_func()
        time.sleep(1)
