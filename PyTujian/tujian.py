from typing import NewType
from datetime import date
import json

UUID = NewType('UUID', str)
TujianColor = NewType('TujianColor', str)
MarkdownRaw = NewType('MarkdownRaw', str)


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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index += 1
            return ('id', self.id)
        elif self.index == 1:
            self.index += 1
            return ('name', self.name)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)

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
    sorts: dict[UUID, TujianSort] = {}

    def __init__(self, raw: list[dict[str, object]]) -> None:
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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self):
            r = self.sorts.values()[self.index]
            self.index += 1
            return r
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)


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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index += 1
            return ('name', self.name)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)

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
    users: dict[str, TujianUser] = {}

    def __init__(self) -> None:
        pass

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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self):
            r = self.users.values()[self.index]
            self.index += 1
            return r
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)


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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index += 1
            return ('width', self.width)
        elif self.index == 1:
            self.index += 1
            return ('height', self.height)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)


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
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index += 1
            return ('theme', self.theme)
        elif self.index == 1:
            self.index += 1
            return ('text', self.text)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)


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
    date: date
    color: TujianPicColor
    user: TujianUser

    def __init__(self, raw: dict, sorts: TujianSortCollection, users: TujianUserCollection) -> None:
        self.id = raw['PID']
        self.title = raw['p_title']
        self.sort = sorts.get(UUID(raw['TID']))
        self.content = MarkdownRaw(raw['p_content'])
        self.url = 'https://s2.images.dailypics.cn' + raw['nativePath']
        self.size = TujianPicSize(
            width=raw['width'],
            height=raw['height']
        )
        self.date = date.fromisoformat(raw['p_date'])
        self.color = TujianPicColor(
            theme=TujianColor(raw['theme_color']),
            text=TujianColor(raw['text_color'])
        )
        self.user = users.get(raw['username'])

    # ==========
    # 实现迭代
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index += 1
            return ('id', self.id)
        elif self.index == 1:
            self.index += 1
            return ('title', self.title)
        elif self.index == 2:
            self.index += 1
            return ('sort', self.sort)
        elif self.index == 3:
            self.index += 1
            return ('content', self.content)
        elif self.index == 4:
            self.index += 1
            return ('url', self.url)
        elif self.index == 5:
            self.index += 1
            return ('size', self.size)
        elif self.index == 6:
            self.index += 1
            return ('date', self.date)
        elif self.index == 7:
            self.index += 1
            return ('color', self.color)
        elif self.index == 8:
            self.index += 1
            return ('user', self.url)
        else:
            raise StopIteration
    # ==========

    def __str__(self) -> str:
        """
        转str，生成json
        """
        return json.dumps(dict(self), ensure_ascii=False)

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
    pics: dict[UUID, TujianPic] = {}

    def __init__(self) -> None:
        pass

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
