import sys
from getopt import gnu_getopt
from typing import Union

from PyTujian.tujian import TujianPicCollection

from .api import TujianV2Api
from .utils import format_size


def ensure_to_download(api: TujianV2Api, pics: TujianPicCollection, env: "CmdEnv") -> Union[bool, TujianPicCollection]:
    e_pics = api.count_exist(pics, env.path_to_dir)
    if env.ignore_exist:
        print(f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张已下载, {len(pics) - len(e_pics)} 张新下载.")
    else:
        print(f"即将下载 {len(pics)} 张图片, 其中 {len(e_pics)} 张重新下载, {len(pics) - len(e_pics)} 张新下载.")
    print(f"这将额外占用 {format_size(pics.total_size() - e_pics.total_size())} 的磁盘空间.")
    if env.ensure_before_download == False:
        return (True, e_pics)
    else:
        ch = input('你确认要继续吗? [Y/n]')
        if ch in ('Y', 'y'):
            return (True, e_pics)
        elif ch in ('N', 'n'):
            return (True, e_pics)
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


def cmd_download_all(api: TujianV2Api, args: list[str], env: "CmdEnv"):
    all = api.get_all()
    return cmd_download(api, all, env)


def cmd_download_today(api: TujianV2Api, args: list[str], env: "CmdEnv"):
    today = api.get_today()
    return cmd_download(api, today, env)


def cmd_download_archive(api: TujianV2Api, args: list[str], env: "CmdEnv"):
    if len(args) == 1:
        sort = api.sorts[env.args[1]]
        if sort is None:
            print('请提供分类的有效 ID')
            return False
        archive = api.get_archive(sort)
        return cmd_download(api, archive, env)
    else:
        print('请提供分类的 ID')
        return False


def cmd_show_sorts(api: TujianV2Api, args: list[str], env: "CmdEnv"):
    for s in api.sorts:
        print(s.name, s.id)


class CmdEnv():

    path_to_dir = 'Tujian'
    ensure_before_download = True
    ignore_exist = True

    args: list[str]
    api: TujianV2Api

    cmd_list = {
        'all': cmd_download_all,
        'archive': cmd_download_archive,
        'sort': cmd_show_sorts,
        'today': cmd_download_today
    }

    def __init__(self) -> None:
        self.api = TujianV2Api()
        opts, args = gnu_getopt(sys.argv[1:],
                                shortopts='p:yf',
                                longopts=['path=']
                                )
        self.args = args

        for o in opts:
            if o[0] in ('-p', '--path'):
                self.path_to_dir = o[1]
            elif o[0] in ('-y'):
                self.ensure_before_download = False
            elif o[0] in ('-f'):
                self.ignore_exist = False

    def run_cmd(self):
        if len(self.args) == 0:
            sys.exit(1)
        target = self.args[0]
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
