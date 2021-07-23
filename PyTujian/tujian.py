from typing import NewType
from datetime import date

UUID = NewType('UUID', str)
TujianColor = NewType('TujianColor', str)
MarkdownRaw = NewType('MarkdownRaw', str)


class TujianSort():
    """
    One class to store picture's sort info
    """
    id: UUID
    name: str

    def __init__(self, id: UUID, name: str) -> None:
        self.id = id
        self.name = name


class TujianSortCollection():
    """
    One class to collect TujianSort
    """
    sorts: dict[UUID, TujianSort] = {}

    def __init__(self, raw: list[dict[str, any]]) -> None:
        for sort in raw:
            id = UUID(sort['TID'])
            self.sorts[id] = TujianSort(id, sort['T_NAME'])

    def get(self, id: UUID) -> TujianSort:
        if id in self.sorts.keys():
            return self.sorts[id]
        else:
            return None


class TujianUser():
    """
    One class to store one user
    """
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class TujianUserCollection():
    """
    One class to collect users
    """
    users: dict[str, TujianUser] = {}

    def __init__(self) -> None:
        pass

    def get(self, name) -> TujianUser:
        if name in self.users.keys():
            return self.users[name]
        else:
            user = TujianUser(name)
            self.users[name] = user
            return user


class TujianPicSize():
    """
    One class to store picture's width and height
    """
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height


class TujianPicColor():
    """
    One class to store picture's theme color
    """
    theme: TujianColor
    text: TujianColor

    def __init__(self, theme: TujianColor, text: TujianColor) -> None:
        self.theme = theme
        self.text = text


class TujianPic():
    """
    One class to store one picture
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


class TujianPicCollection():
    """
    One class to collect TujianPic
    """
    pics: dict[UUID, TujianPic] = {}

    def __init__(self) -> None:
        pass

    def get(self, id: UUID) -> TujianPic:
        if id in self.pics.keys():
            return self.pics[id]
        else:
            return None

    def put(self, pic: TujianPic) -> None:
        if not pic.id in self.pics.keys():
            self.pics[pic.id] = pic
