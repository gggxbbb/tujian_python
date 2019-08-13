import sys
from . import print2

message = [
    'TujianP 第三方 Tujian 命令行工具',
    '',
    '命令:',
    'today               下载今日图片',
    'sort                加载分类列表',
    'archive <TID>       根据 TID 获取图片, 不含当日图片',
    'all                 获取所有图片',
    #'img <PID>           根据 PID 获取图片',
    #'search <KEY>        搜索图片',
    'help                查看帮助',
    'path                获得图片保存目录',
    '',
    '值:',
    'TID                 分类的 UUID , 使用 sort 获取',
    'PID                 图片的 UUID , 获取方式请随意',
    'KEY                 图片的 关键字',
    '',
    '使用 help <命令> 查看详细内容'
]

detail = {
    'today':['...'],
    'sort':['...'],
    'archive':['...'],
    'all':['...'],
    'img':['...'],
    'search':['...'],
    'help': ['查看帮助']
}


def TujianHelper(par):
    try:
        for v in detail[par[1]]:
            print(v)
        sys.exit()
    except IndexError:
        for v in message:
            print(v)
        sys.exit()
    except KeyError:
        print2.error('找不到这个命令')
        sys.exit(1)