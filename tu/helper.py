import sys
from . import print2

message = [
    'TujianP 第三方 Tujian 命令行工具',
    '',
    '用法:',
    'python3 -m tu -h -p <path> --help --path=<path> <命令> [参数1 [参数2] ... ]',
    '',
    '命令:',
    'today               下载今日图片',
    'sort                加载分类列表',
    'archive <TID>       根据 TID 获取图片, 不含当日图片',
    'all                 获取所有图片',
    'info <PID>          根据 PID 查询图片信息',
    'upload <file>       根据配置文件批量上传'
    #'img <PID>           根据 PID 获取图片',
    #'search <KEY>        搜索图片',
    'help                查看帮助',
    'path                获取图片保存目录',
    '',
    '值:',
    'TID                 分类的 UUID , 使用 sort 获取',
    'PID                 图片的 UUID , 获取方式请随意',
    'KEY                 图片的 关键字',
    'file                一个文件的路径',
    '',
    '参数:',
    '-h --help           查看帮助',
    '-p <path>           自定义存储路径(会自动追加 Tujian 文件夹)',
    '-path=<path>        同上'
    '',
    '使用 help <命令> 查看详细内容'
]

detail = {
    'today': [
        '获得今日的所有图片',
        '如果今天啥都没更,拿会获取上一天的',
        '毕竟 API 返回的就是这样'
    ],
    'sort': [
        '获取所有的分类',
        '格式为:',
        '分类名 -- TID'
    ],
    'archive': [
        '需要参数 TID',
        '根据 TID 获得分类下图片归档',
        '不含当日图片',
        'API 返回就这样'
    ],
    'all': [
        '获得所有图片'
    ],
    'info': [
        '需要参数 PID',
        '查询指定图片的信息'
    ],
    'upload':[
        '需要参数 file',
        '批量投稿',
        '详情请访问 https://gggxbbb.github.io/tujian_python/'
    ],
    'img': ['...'],
    'search': ['...'],
    'help': [
        '查看帮助'
    ]
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
