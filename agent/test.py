from threading import current_thread
from time import sleep

lines = [
    'acb',
    'qwbe',
    'jklcjkl',
    'hhhhbbbbb',
    'asdasdasdcb',

]


def pisi_u_fajl(file_path):
    f = open(file_path, 'a')
    i = 0
    while True:
        sleep(1)
        f.write("%s %d\n" % (lines[i % 5], i))
        f.flush()
        i += 1


if __name__ == '__main__':
    pisi_u_fajl('log.txt')