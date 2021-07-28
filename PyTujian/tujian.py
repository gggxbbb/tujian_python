import datetime
import json
from typing import Dict, List, NewType

UUID = NewType('UUID', str)
TujianColor = NewType('TujianColor', str)
MarkdownRaw = NewType('MarkdownRaw', str)


class TujianJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TujianSort):
            return dict(o)
        elif isinstance(o, TujianUser):
            return dict(o)
        elif isinstance(o, TujianPic):
            return dict(o)
        elif isinstance(o, TujianPicSize):
            return dict(o)
        elif isinstance(o, TujianPicColor):
            return dict(o)
        elif isinstance(o, TujianSortCollection):
            return o.sorts
        elif isinstance(o, TujianUserCollection):
            return o.users
        elif isinstance(o, TujianPicCollection):
            return o.pics
        elif isinstance(o, datetime.date):
            return o.isoformat()
        else:
            return super().default(o)


class TujianSort():
    """
    定义图片分类
    """
    id: UUID  # 分类 id
    name: str  # 分类 中文名称

    def __init__(self, id: UUID, name: str) -> None:
        self.id = id
        self.name = name

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return ('id', self.id)
        elif self._index == 1:
            self._index += 1
            return ('name', self.name)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)

    def __eq__(self, o: object) -> bool:
        """
        处理 ==
        """
        if type(self) == type(o):
            return self.id == o.id
        else:
            return self.id == str(o)


class TujianSortCollection():
    """
    存储图片分类
    """
    sorts: Dict[UUID, TujianSort]

    def __init__(self, raw: List[Dict[str, object]]) -> None:
        self.sorts = {}
        for sort in raw:
            id = UUID(sort['TID'])
            self.sorts[id] = TujianSort(id, sort['T_NAME'])

    def get(self, id: UUID) -> TujianSort:
        """
        根据id获取分类，不存在则返回 None
        """
        if id in self.sorts.keys():
            return self.sorts[id]
        else:
            return None

    def __getitem__(self, key: UUID):
        """
        使用索引取值
        """
        return self.get(key)

    def __len__(self):
        """
        使用len()获取数量
        """
        return len(self.sorts)

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self):
            r = list(self.sorts.values())[self._index]
            self._index += 1
            return r
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)


class TujianUser():
    """
    定义用户
    """
    # id: UUID # 用户 id
    name: str  # 用户名

    def __init__(self, name: str) -> None:
        self.name = name

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return ('name', self.name)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)

    def __eq__(self, o: object) -> bool:
        """
        处理 ==
        """
        if type(self) == type(o):
            return self.name == o.id
        else:
            return self.name == str(o)


class TujianUserCollection():
    """
    存储用户
    """
    users: Dict[str, TujianUser]

    def __init__(self) -> None:
        self.users = {}

    def get(self, name) -> TujianUser:
        """
        根据用户名获取用户，不存在则新建
        """
        if name in self.users.keys():
            return self.users[name]
        else:
            user = TujianUser(name)
            self.users[name] = user
            return user

    def __getitem__(self, key: UUID):
        """
        使用索引取值
        """
        return self.get(key)

    def __len__(self):
        """
        使用len()获取数量
        """
        return len(self.users)

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self):
            r = list(self.users.values())[self._index]
            self._index += 1
            return r
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)


class TujianPicSize():
    """
    定义图片大小
    """
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return ('width', self.width)
        elif self._index == 1:
            self._index += 1
            return ('height', self.height)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)


class TujianPicColor():
    """
    定义图片颜色
    """
    theme: TujianColor
    text: TujianColor

    def __init__(self, theme: TujianColor, text: TujianColor) -> None:
        self.theme = theme
        self.text = text

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return ('theme', self.theme)
        elif self._index == 1:
            self._index += 1
            return ('text', self.text)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)


class TujianPic():
    """
    定义 Tujian 的图
    """
    id: UUID
    title: str
    sort: TujianSort
    content: MarkdownRaw
    url: str
    size: TujianPicSize
    date: datetime.date
    color: TujianPicColor
    user: TujianUser
    file_size: int
    file_type: str

    def __init__(self, raw: dict, sorts: TujianSortCollection, users: TujianUserCollection, file_size: int = None, file_type: str = None) -> None:
        self.id = raw['PID']
        self.title = raw['p_title']
        self.sort = sorts.get(UUID(raw['TID']))
        self.content = MarkdownRaw(raw['p_content'])
        self.url = 'https://s2.images.dailypics.cn' + raw['nativePath']
        self.size = TujianPicSize(
            width=raw['width'],
            height=raw['height']
        )
        self.date = datetime.date.fromisoformat(raw['p_date'])
        self.color = TujianPicColor(
            theme=TujianColor(raw['theme_color']),
            text=TujianColor(raw['text_color'])
        )
        self.user = users.get(raw['username'])
        self.file_size = file_size
        self.file_type = file_type

    def init(self, file_size: int, file_type: str):
        self.file_size = file_size
        self.file_type = file_type

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return ('id', self.id)
        elif self._index == 1:
            self._index += 1
            return ('title', self.title)
        elif self._index == 2:
            self._index += 1
            return ('sort', self.sort)
        elif self._index == 3:
            self._index += 1
            return ('content', self.content)
        elif self._index == 4:
            self._index += 1
            return ('url', self.url)
        elif self._index == 5:
            self._index += 1
            return ('size', self.size)
        elif self._index == 6:
            self._index += 1
            return ('date', self.date)
        elif self._index == 7:
            self._index += 1
            return ('color', self.color)
        elif self._index == 8:
            self._index += 1
            return ('user', self.user)
        elif self._index == 9:
            self._index += 1
            return ('file_size', self.file_size)
        elif self._index == 10:
            self._index += 1
            return ('file_type', self.file_type)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)

    def __eq__(self, o: object) -> bool:
        """
        处理 ==
        """
        if type(self) == type(o):
            return self.id == o.id
        else:
            return self.id == str(o)


class TujianPicCollection():
    """
    存储图
    """
    pics: Dict[UUID, TujianPic]

    def __init__(self) -> None:
        self.pics = {}

    # ==========
    # 实现迭代
    _index: int

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self):
            r = list(self.pics.values())[self._index]
            self._index += 1
            return r
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(self, ensure_ascii=False, cls=TujianJSONEncoder)

    def get(self, id: UUID) -> TujianPic:
        """
        根据 id 获取图，不存在则返回 None
        """
        if id in self.pics.keys():
            return self.pics[id]
        else:
            return None

    def put(self, pic: TujianPic) -> None:
        """
        存入图
        """
        if not pic.id in self.pics.keys():
            self.pics[pic.id] = pic

    def total_size(self) -> int:
        t = 0
        for i in self.pics.values():
            t += i.file_size
        return t

    def __getitem__(self, key: UUID):
        """
        使用索引取值
        """
        return self.get(key)

    def __setitem__(self, key: UUID, value: TujianPic):
        """
        使用索引赋值
        """
        if value.id == key:
            self.put(value)

    def __len__(self):
        """
        使用len()获取数量
        """
        return len(self.pics)

    def __add__(self, o):
        if isinstance(o, TujianPicCollection):
            for pic in o:
                self.put(pic)
            return self
        else:
            raise ValueError(f'Can not add {type(o)} to TujianPicCollection')

    def __sub__(self, o):
        if isinstance(o, TujianPicCollection):
            for pic in o:
                del self.pics[pic.id]
            return self
        else:
            raise ValueError(f'Can not add {type(o)} to TujianPicCollection')
