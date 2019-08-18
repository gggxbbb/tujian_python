import sys
import os
import signal
from .helper import TujianHelper
from .tools import printSort,getToday,getArchive,getAll,printInfo
from . import print2

par = sys.argv[1:]

dir = './Tujian/'
if not os.path.isdir(dir):
    os.makedirs(dir)
path = os.path.abspath(dir)

def exitTujian(signum,frame):
    print2.waring('操作终止')
    sys.exit()

signal.signal(signal.SIGINT,exitTujian)
signal.signal(signal.SIGTERM,exitTujian)

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
    getArchive(par,path)

elif key == 'sort':
    printSort()

elif key == 'all':
    getAll(path)

elif key == 'info':
    printInfo(par)

else:
    print2.error('找不到这个命令')
    print('使用 help 查看帮助')
    sys.exit(1)

sys.exit()