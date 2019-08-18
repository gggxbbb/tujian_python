from urllib import request
from urllib.request import urlretrieve
from urllib import error
from urllib import parse
from . import print2
import json
import sys

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def get(url):
    try:
        req = request.Request(url, headers=header)
        data = request.urlopen(req).read().decode('utf-8')
        return data
    except:
        print2.error('加载失败')
        sys.exit(1)


def getJson(url):
    return json.loads(get(url))


def downloadB(url, path):
    try:
        req = request.Request(url, headers=header)
        data = request.urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
    except:
        print2.error('下载失败')
        sys.exit(1)
