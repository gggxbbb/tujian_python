import os
from datetime import datetime
import time

import pytz
from requests import Session
from requests.models import CaseInsensitiveDict
from tqdm import tqdm

from .tujian import *


class BasicApi():
    """
    基本 API
    """

    _api_root: str
    _session = Session()

    def __init__(self) -> None:
        self._session = Session()
        pass


class TujianV2Api(BasicApi):
    """
    TujianV2 API 适配器, 内置进度条
    """

    _api_root = "https://v2.api.dailypics.cn/"
    sorts: TujianSortCollection
    users: TujianUserCollection
    block_char = {
        '\\': '-',
        '/': '-',
        ':': '-',
        '*': '-',
        '?': '-',
        '<': '-',
        '>': '-',
        '|': '-',
        '"': '-'
    }
    headers_cache_path = os.path.join(
        os.path.expanduser('~'), '.pytujian/headers/')

    def __init__(self, auto_init=True) -> None:
        """
        构建 API 对象

        若设置 `auto_init=True` (默认值), 将自动获取分类信息和用户列表, 否则需手动 `.init()`
        """
        super().__init__()
        if not os.path.isdir(self.headers_cache_path):
            os.makedirs(self.headers_cache_path)
        self._session.headers.update(
            {'User-Agent': f"PyTujian/{datetime.datetime.now(pytz.timezone('PRC')).strftime('%Y%m%d%H')}"})
        if auto_init:
            self.init()

    def init(self):
        """
        初始化
        """
        self.__get_sorts()
        self.__get_users()

    def __get_sorts(self):
        """
        初始化分类信息
        """
        api_url = self._api_root + 'sort'
        api_result = self._session.get(api_url).json()['result']
        self.sorts = TujianSortCollection(api_result)

    def __get_users(self):
        """
        初始化用户信息
        """
        self.users = TujianUserCollection()

    def __get_pic_headers(self, pic: TujianPic) -> CaseInsensitiveDict:
        """
        获取 header
        """
        cache = os.path.join(self.headers_cache_path, pic.id)
        if os.path.isfile(cache):
            with open(cache, 'r', encoding='utf8') as f:
                pic_header = CaseInsensitiveDict(json.loads(f.read()))
                f.close()
            return pic_header
        else:
            pic_req = self._session.head(pic.url)
            with open(cache, 'w', encoding='utf8') as f:
                f.write(json.dumps(dict(pic_req.headers)))
                f.close()
            return pic_req.headers

    def build_tujian_pic_colletcion(self, raw: list, desc='加载图片列表') -> TujianPicCollection:
        """
        根据 API 返回的原始数据生成 TujianPicCollection
        """
        _tpc = TujianPicCollection()
        with tqdm(total=len(raw), leave=False, desc=desc, unit='pic', unit_scale=False) as p:
            for i in raw:
                _pic = TujianPic(raw=i, sorts=self.sorts, users=self.users)
                _header = self.__get_pic_headers(_pic)
                _pic.init(
                    file_size=int(_header['content-length']),
                    file_type=str(_header['content-type'])
                )
                _tpc.put(_pic)
                p.update()
        return _tpc

    def format_file_name(self, raw: TujianPic) -> str:
        """
        获取文件名
        """
        file_type = raw.file_type.split('/')[-1]
        file_name = f"{raw.date.isoformat()}-{raw.sort.name}_{raw.title}_{raw.id}.{raw.user.name}.{file_type}"
        for (k, v) in self.block_char.items():
            file_name = file_name.replace(k, v)
        return file_name

    def get_today(self) -> TujianPicCollection:
        """
        加载今日图片
        """
        api_url = self._api_root + 'today'
        api_req = self._session.get(api_url)
        api_result = api_req.json()
        return self.build_tujian_pic_colletcion(api_result, desc='加载今日图片')

    def get_archive(self, sort: TujianSort) -> TujianPicCollection:
        """
        加载图片归档
        """
        tpc = TujianPicCollection()
        with tqdm(leave=True, desc=f'加载{sort.name}列表', unit='page', unit_scale=False) as p:
            first_page = self._session.get('https://v2.api.dailypics.cn/list', params={
                'page': 1,
                'size': 20,
                'sort': sort.id
            }).json()
            p.total = first_page['maxpage']
            tpc += self.build_tujian_pic_colletcion(
                first_page['result'], desc='加载第1页')
            p.update()
            for page in range(2, first_page['maxpage']+1):
                res = self._session.get('https://v2.api.dailypics.cn/list', params={
                    'page': page,
                    'size': 20,
                    'sort': sort.id
                }).json()
                tpc += self.build_tujian_pic_colletcion(
                    res['result'], desc=f'加载第{page}页')
                p.update()
        return tpc

    def get_all(self) -> TujianPicCollection:
        """
        加载所有图片
        """
        with tqdm(total=len(self.sorts)+1, leave=True, desc='加载所有图片', unit='item', unit_scale=False) as p:
            tpc = self.get_today()
            p.update()
            for sort in self.sorts:
                tpc += self.get_archive(sort)
                p.update()
        return tpc

    def __build_file_path(self, raw: TujianPic, path_to_dir: str = None) -> str:
        if path_to_dir is not None:
            if not os.path.isdir(path_to_dir):
                os.makedirs(path_to_dir)
            pic_path = os.path.join(
                path_to_dir, self.format_file_name(raw))
        else:
            pic_path = self.format_file_name(raw)
        return pic_path

    def __if_exist(self, raw: TujianPic, pic_path: str = None) -> bool:
        if os.path.isfile(pic_path):
            if os.path.getsize(pic_path) == raw.file_size:
                return True
        return False

    def download_pic(self, raw: TujianPic, path_to_dir: str = None, ignore_exist: bool = True):
        """
        下载图片
        """
        with tqdm(total=raw.file_size, leave=False, desc=raw.title, unit='B', unit_scale=True, unit_divisor=1024) as p:
            pic_path = self.__build_file_path(raw, path_to_dir)
            if ignore_exist:
                if self.__if_exist(raw, pic_path):
                    p.update(raw.file_size)
                    time.sleep(0.01)
                    return
            pic_res = self._session.get(raw.url, stream=True)
            with open(pic_path, 'wb') as f:
                for chunk in pic_res.iter_content(chunk_size=512):
                    f.write(chunk)
                    p.update(len(chunk))

    def download_pic_collection(self, raw: TujianPicCollection, path_to_dir: str = None, ignore_exist: bool = True):
        """
        下载图片集
        """
        with tqdm(total=len(raw), leave=True, desc='下载中', unit='pic', unit_scale=False) as p:
            for pic in raw:
                self.download_pic(pic, path_to_dir, ignore_exist)
                p.update(1)

    def count_exist(self, raw: TujianPicCollection, path_to_dir: str = None) -> TujianPicCollection:
        tpc = TujianPicCollection()
        for pic in raw:
            path = self.__build_file_path(pic, path_to_dir)
            if self.__if_exist(pic, path):
                tpc.put(pic)
        return tpc
