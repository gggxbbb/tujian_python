import sys
from datetime import datetime
from getopt import GetoptError, gnu_getopt
from typing import List, Union

import pytz

from PyTujian.tujian import TujianPicCollection

from .api import UUID, TujianV2Api
from .utils import format_size


def ensure_to_download(api: TujianV2Api, pics: TujianPicCollection, env: "CmdEnv") -> Union[bool, TujianPicCollection]:
    if len(pics) == 0:
        print('没有可供下载的图片')
        return (False, None)
    e_pics = api.count_exist(pics, env.path_to_dir)
    if env.ignore_exist:
        print(
            f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张已下载, {len(pics) - len(e_pics)} 张新下载.")
    else:
        print(
            f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张重新下载, {len(pics) - len(e_pics)} 张新下载.")
    print(
        f"这将额外占用 {format_size(pics.total_size() - e_pics.total_size())} 的磁盘空间.")
    if env.ensure_before_download == False:
        return (True, e_pics)
    else:
        ch = input('你确认要继续吗? [Y/n]')
        if ch in ('Y', 'y'):
            return (True, e_pics)
        elif ch in ('N', 'n'):
            return (False, e_pics)
        else:
            print('看起来你似乎还没明白将发生什么, 那就再问一次: ')
            return ensure_to_download(api, pics, env)


def cmd_download(api: TujianV2Api, pics: TujianPicCollection, env: "CmdEnv"):
    ch, e_pics = ensure_to_download(api, pics, env)
    if ch:
        if env.ignore_exist:
            pics -= e_pics
        api.download_pic_collection(pics, env.path_to_dir, env.ignore_exist)
        print('完成')
    return ch


def cmd_download_all(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    print('正在加载图片列表...')
    all = api.get_all()
    print('完成')
    print()
    return cmd_download(api, all, env)


def cmd_download_today(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    print('正在加载今日列表...')
    today = api.get_today()
    print('完成')
    print()
    today_date = datetime.now(pytz.timezone('PRC')).strftime('%Y-%m-%d')
    not_today = TujianPicCollection()
    for pic in today:
        if not pic.date.isoformat() == today_date:
            not_today.put(pic)
    if not len(not_today) == 1:
        print(
            f'在总共 {len(today)} 张图片中, 有 {len(not_today)} 张不是今日({today_date})更新的:')
        for pic in not_today:
            print(f'{pic.sort.name}: {pic.title} 更新于 {pic.date.isoformat()}')
        if not env.only_today:
            print('你可以使用参数 -s 来只下载今日更新的图片')
        print()
    if env.only_today:
        return cmd_download(api, today - not_today, env)
    else:
        return cmd_download(api, today, env)


def cmd_download_one(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        try:
            pic = api.get_one(UUID(args[0]))
        except:
            print('参数异常, 请提供图片的有效 ID')
            return False
        tpc = TujianPicCollection()
        tpc.put(pic)
        return cmd_download(api, tpc, env)
    else:
        print('参数异常, 请提供图片的 ID')
        return True


def cmd_download_archive(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        sort = api.sorts[env.args[1]]
        if sort is None:
            print('参数异常, 请提供分类的有效 ID')
            return False
        print(f'正在加载{sort.name}列表...')
        archive = api.get_archive(sort)
        print('完成')
        print()
        return cmd_download(api, archive, env)
    else:
        print('参数异常, 请提供分类的 ID')
        return False


def cmd_show_sorts(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    for s in api.sorts:
        print(s.name, s.id)
    return True


def cmd_show_info(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        try:
            pic = api.get_one(UUID(args[0]))
        except Exception as e:
            print(e)
            print('参数异常, 请提供图片的有效 ID')
            return False
        print(pic.title)
        print(f'{pic.date.isoformat()}|{pic.sort.name}')
        print('')
        print('以下为未处理的 Markdown 格式图片介绍:')
        print(pic.content)
        print()
        print(f'访问 https://www.dailypics.cn/member/{pic.id} 查看更多信息')
    else:
        print('参数异常, 请提供图片的 ID')
        return True


class CmdEnv():

    path_to_dir = 'Tujian'
    ensure_before_download = True
    ignore_exist = True
    only_today = False

    args: List[str]
    api: TujianV2Api

    cmd_list = {
        'all': cmd_download_all,
        'archive': cmd_download_archive,
        'sort': cmd_show_sorts,
        'today': cmd_download_today,
        'info': cmd_show_info,
        'get': cmd_download_one
    }

    cmd_intr = [
        "PyTujian",
        "一个简易的 Tujian 命令行工具",
        "图片默认保存在当前目录下的 Tujian 文件夹",
        "",
        "all            获取所有图片",
        "archive <id>   获取指定分类的图片",
        "sort           打印分类列表",
        "today          获取今天图片",
        "info <id>      获取图片详情",
        "get <id>       下载单张图片"
        "",
        "-p <path>      指定图片存储目录",
        "--path=        指定图片存储目录",
        "-y             跳过下载确认",
        "-f             覆盖本地已存在图片",
        "-s             today 命令只下载今日图片",
        "",
        "访问 https://docs.evax.top/docs/pytujian 查看详细文档"
    ]

    def show_help(self):
        for msg in self.cmd_intr:
            print(msg)

    def __init__(self) -> None:
        try:
            self.api = TujianV2Api()
        except Exception as e:
            print('初始化 API 失败:')
            print('\n'.join(e.args))
        try:
            opts, args = gnu_getopt(sys.argv[1:],
                                    shortopts='p:yfs',
                                    longopts=['path=']
                                    )
        except GetoptError:
            print('参数异常')
            sys.exit(1)
        self.args = args

        for o in opts:
            if o[0] in ('-p', '--path'):
                self.path_to_dir = o[1]
            elif o[0] in ('-y'):
                self.ensure_before_download = False
            elif o[0] in ('-f'):
                self.ignore_exist = False
            elif o[0] in ('-s'):
                self.only_today = True

    def run_cmd(self):
        if len(self.args) == 0:
            self.show_help()
            sys.exit(0)
        target = self.args[0]
        if target == 'help':
            self.show_help()
            sys.exit(0)
        if not target in self.cmd_list.keys():
            print(f'不支持的命令: {target}')
            sys.exit(1)
        try:
            re = self.cmd_list[target](self.api, self.args[1:], self)
        except Exception as e:
            print('看起来似乎出了什么问题:')
            print('\n'.join(e.args))
            sys.exit(1)
        if re:
            sys.exit(0)
        else:
            sys.exit(1)
