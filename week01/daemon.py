import sys
import os
import time


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='dev/null'):
    try:

        # 创建子进程
        pid = os.fork()

        if pid > 0:
            # exit first parent
            # 父进程先于子进程exit，会使子进程变为孤儿进程，
            # 这样子进程会被 init 这个用户级守护进程收养
            sys.exit(0)

    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    # decouple from parent environment
    # 从父进程环境脱离
    # chdir 确保进程不占用任何目录，否则不能 umount
    os.chdir('/')
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            # 第二个父进程退出
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
        sys.exit(1)

    # redirect standard file descriptors
    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')

    # dup2 函数原子化关闭和复制文件描述符
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def test():
    print('test')
    sys.stdout.write('Daemon started with pid %d\n' % os.getpgid())
    sys.stdout.write(f'{time.ctime()}\n')
    sys.stdout.flush()


if __name__ == '__main__':
    print('ok')
    daemonize('/dev/null', '/tmp/d1.log', '/dev/null')
    test()
