from urllib import request
from urllib.request import urlretrieve
from urllib import error
from urllib import parse
import imghdr
import mimetypes
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
        return 1


def getJson(url):
    try:
        return json.loads(get(url))
    except:
        return 1

def downloadB(url, path):
    try:
        req = request.Request(url, headers=header)
        data = request.urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
        return 0
    except:
        return 1


def uploadB(url, path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
            f.close()
        header2 = header
        header2['Content-Type'] = mimetypes.guess_type(path)[0]
        req = request.Request(url, data, headers=header2)
        data2 = request.urlopen(req).read().decode('utf-8')
        return data2
    except:
        return 1


def uploadBJSON(url, path):
    try:
        return json.loads(uploadB(url, path))
    except:
        return 1

def post(url, data):
    try:
        data3 = bytes(json.dumps(data), encoding='utf-8')
        req = request.Request(url, data3, headers=header)
        data2 = request.urlopen(req).read().decode('utf-8')
        return data2
    except:
        return 1


def postJSON(url, data):
    try:
        return json.loads(post(url, data))
    except:
        return 1