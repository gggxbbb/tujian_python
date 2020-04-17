import sys
import os
import signal
from getopt import getopt
from .helper import TujianHelper
from .tools import printSort, getToday, getArchive, getAll, printByPID, getByPID
from .upload import upoladPics
from .check import check
from . import print2

pars = sys.argv[1:]
try:
    opt, par = getopt(pars, 'hp:', ['help', 'path='])
except:
    TujianHelper(pars)

dir = './Tujian/'
path = os.path.abspath(dir)


def exitTujian(signum, frame):
    raise KeyboardInterrupt('操作被用户终止')


signal.signal(signal.SIGINT, exitTujian)
signal.signal(signal.SIGTERM, exitTujian)

for o, a in opt:
    if o in ('-h', '--help'):
        par2 = ['help'] + par
        TujianHelper(par2)
        sys.exit()
    elif o in ('-p', '--path'):
        path = os.path.join(a, 'Tujian')

if not os.path.isdir(path):
    os.makedirs(path)

try:
    key = par[0]
except IndexError:
    TujianHelper(par)
    sys.exit()

if key == 'help':
    TujianHelper(par)

elif key == 'path':
    print(path)

elif key == 'today':
    getToday(path)

elif key == 'archive':
    getArchive(par, path)

elif key == 'sort':
    printSort()

elif key == 'all':
    getAll(path)

elif key == 'info':
    printByPID(par)

elif key == 'upload':
    upoladPics(par)

elif key == 'get':
    getByPID(par,path)

elif key == 'check':
    check(par)

else:
    print2.error('找不到这个命令')
    print('使用 help 查看帮助')
    sys.exit(1)

sys.exit()
