from requests import Session
from datetime import datetime
import pytz
from requests.models import CaseInsensitiveDict
from tqdm import tqdm
import os

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
        '|': '-'
    }

    def __init__(self, auto_init=True) -> None:
        """
        构建 API 对象

        若设置 `auto_init=True` (默认值), 将自动获取分类信息和用户列表, 否则需手动 `.init()`
        """
        super().__init__()
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

    def __get_pic_headers(self, url: str) -> CaseInsensitiveDict:
        """
        获取 header
        """
        pic_req = self._session.head(url)
        return pic_req.headers

    def build_tujian_pic_colletcion(self, raw: list) -> TujianPicCollection:
        """
        根据 API 返回的原始数据生成 TujianPicCollection
        """
        _tpc = TujianPicCollection()
        with tqdm(total=len(raw), leave=False, desc='加载图片列表', unit='pic') as p:
            for i in raw:
                _pic = TujianPic(raw=i, sorts=self.sorts, users=self.users)
                _header = self.__get_pic_headers(_pic.url)
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
        return self.build_tujian_pic_colletcion(api_result)

    def download_pic(self, raw: TujianPic, path_to_dir: str = None, ignore_exist: bool = True):
        """
        下载图片
        """
        with tqdm(total=raw.file_size, leave=False, desc=raw.title, unit='B', unit_scale=True, unit_divisor=1024) as p:
            pic_res = self._session.get(raw.url, stream=True)
            if path_to_dir is not None:
                if not os.path.isdir(path_to_dir):
                    os.makedirs(path_to_dir)
                pic_path = os.path.join(
                    path_to_dir, self.format_file_name(raw))
            else:
                pic_path = self.format_file_name(raw)
            if ignore_exist:
                if os.path.isfile(pic_path):
                    return
            with open(pic_path, 'wb') as f:
                for chunk in pic_res.iter_content(chunk_size=512):
                    f.write(chunk)
                    p.update(len(chunk))

    def download_pic_collection(self, raw: TujianPicCollection, path_to_dir: str = None, ignore_exist: bool = True):
        """
        下载图片集
        """
        with tqdm(total=len(raw), leave=False, desc='下载中',unit='pic' ,unit_scale=True) as p:
            for pic in raw:
                self.download_pic(pic, path_to_dir, ignore_exist)
                p.update(1)