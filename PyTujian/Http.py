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


flags = ['|','/','-','\\']


def progress(done,size,total):
    pre =100.0 * done * size / total
    down = done * size
    print2.print2.message('>%s %0.2f%% [%s%s]  @ %0.2fKB/%0.2fKB\r'%(flags[int(pre)%4],pre,'#'*int(pre/10),'.'*int(10-pre/10),down/1024,total/1024))
    if pre > 100:
        print2.print2.message('\r')



def get(url):
    try:
        req = request.Request(url, headers=header)
        data = request.urlopen(req).read().decode('utf-8')
        return data
    except KeyboardInterrupt:
        sys.exit()
    except:
        return 1


def getJson(url):
    re = get(url)
    if re == 1:
        return 1
    return json.loads(re)

def downloadB(url, path):
    try:
        request.urlretrieve(url, path, progress)
        return 0
    except KeyboardInterrupt:
        sys.exit()
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
    except KeyboardInterrupt:
        sys.exit()
    except:
        return 1


def uploadBJSON(url, path):
    re = uploadB(url,path)
    if re == 1:
        return re
    return json.loads(re)

def post(url, data):
    try:
        data3 = bytes(json.dumps(data), encoding='utf-8')
        req = request.Request(url, data3, headers=header)
        data2 = request.urlopen(req).read().decode('utf-8')
        return data2
    except KeyboardInterrupt:
        sys.exit()
    except:
        return 1


def postJSON(url, data):
    re = post(url, data)
    if re == 1:
        return 1
    return json.loads(post(url, data))
