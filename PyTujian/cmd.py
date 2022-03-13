import sys
from datetime import datetime
from getopt import GetoptError, gnu_getopt
from typing import List, Union
import requests
import io

from rich.console import Console
from rich.text import Text
from rich.color import Color
from rich.style import Style
from rich.markdown import Markdown
from PIL import Image

import numpy as np

import pytz

from PyTujian.tujian import TujianPicCollection

from .api import UUID, TujianV2Api
from .utils import format_size


def ensure_to_download(api: TujianV2Api, pics: TujianPicCollection, env: "CmdEnv") -> Union[bool, TujianPicCollection]:
    if len(pics) == 0:
        env.console.print('没有可供下载的图片')
        return (False, None)
    e_pics = api.count_exist(pics, env.path_to_dir)
    if env.ignore_exist:
        env.console.print(
            f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张已下载, {len(pics) - len(e_pics)} 张新下载.")
    else:
        env.console.print(
            f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张重新下载, {len(pics) - len(e_pics)} 张新下载.")
    env.console.print(
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
            env.console.print('看起来你似乎还没明白将发生什么, 那就再问一次: ')
            return ensure_to_download(api, pics, env)


def cmd_download(api: TujianV2Api, pics: TujianPicCollection, env: "CmdEnv"):
    ch, e_pics = ensure_to_download(api, pics, env)
    if ch:
        if env.ignore_exist:
            pics -= e_pics
        api.download_pic_collection(pics, env.path_to_dir, env.ignore_exist)
        env.console.print('完成')
    return ch


def cmd_download_all(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    env.console.print('正在加载图片列表...')
    all = api.get_all()
    env.console.print('完成')
    env.console.print()
    return cmd_download(api, all, env)


def cmd_download_today(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    env.console.print('正在加载今日列表...')
    today = api.get_today()
    env.console.print('完成')
    env.console.print()
    today_date = datetime.now(pytz.timezone('PRC')).strftime('%Y-%m-%d')
    not_today = TujianPicCollection()
    for pic in today:
        if not pic.date.isoformat() == today_date:
            not_today.put(pic)
    if not len(not_today) == 1:
        env.console.print(
            f'在总共 {len(today)} 张图片中, 有 {len(not_today)} 张不是今日({today_date})更新的:')
        for pic in not_today:
            env.console.print(f'{pic.sort.name}: {pic.title} 更新于 {pic.date.isoformat()}')
        if not env.only_today:
            env.console.print('你可以使用参数 -s 来只下载今日更新的图片')
        env.console.print()
    if env.only_today:
        return cmd_download(api, today - not_today, env)
    else:
        return cmd_download(api, today, env)


def cmd_download_one(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        try:
            pic = api.get_one(UUID(args[0]))
        except:
            env.console.print('参数异常, 请提供图片的有效 ID')
            return False
        tpc = TujianPicCollection()
        tpc.put(pic)
        return cmd_download(api, tpc, env)
    else:
        env.console.print('参数异常, 请提供图片的 ID')
        return True


def cmd_download_archive(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        sort = api.sorts[env.args[1]]
        if sort is None:
            env.console.print('参数异常, 请提供分类的有效 ID')
            return False
        env.console.print(f'正在加载{sort.name}列表...')
        archive = api.get_archive(sort)
        env.console.print('完成')
        env.console.print()
        return cmd_download(api, archive, env)
    else:
        env.console.print('参数异常, 请提供分类的 ID')
        return False


def cmd_show_sorts(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    for s in api.sorts:
        env.console.print(s.name, s.id)
    return True


def cmd_show_info(api: TujianV2Api, args: List[str], env: "CmdEnv"):
    if len(args) == 1:
        try:
            pic = api.get_one(UUID(args[0]))
        except Exception:
            env.console.print('参数异常, 请提供图片的有效 ID')
            env.console.print_exception()
            return False
        msg = f"# {pic.title}\n  \n{pic.content}\n  \n"
        msg2 = f"> 分类：{pic.sort.name}  \n> 投稿：{pic.user.name}  \n> 日期: {pic.date.isoformat()}  \n> 大小：{format_size(pic.file_size)}  \n> 长宽：{pic.size.width}x{pic.size.height}\n  \n详细信息：[https://www.dailypics.cn/member/{pic.id}](https://www.dailypics.cn/member/{pic.id})"
        md = Markdown(msg)
        md2 = Markdown(msg2)
        env.console.print(md)
        env.console.print_json(str(pic), indent=4, ensure_ascii=False)
        env.console.print(md2)
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
    console: Console

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
            self.console.print(msg)

    def __init__(self) -> None:
        try:
            self.api = TujianV2Api()
        except Exception as e:
            self.console.print('初始化 API 失败:')
            self.console.print('\n'.join(e.args))
        try:
            opts, args = gnu_getopt(sys.argv[1:],
                                    shortopts='p:yfs',
                                    longopts=['path=']
                                    )
        except GetoptError:
            self.console.print('参数异常')
            sys.exit(1)
        self.args = args
        self.console = Console(color_system='truecolor', force_terminal=True, force_interactive=True)

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
            self.console.print(f'不支持的命令: {target}')
            sys.exit(1)
        try:
            re = self.cmd_list[target](self.api, self.args[1:], self)
        except Exception:
            self.console.print('看起来似乎出了什么问题:')
            self.console.print_exception()
            sys.exit(1)
        if re:
            sys.exit(0)
        else:
            sys.exit(1)
