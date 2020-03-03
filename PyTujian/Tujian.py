from . import Http, print2
import sys


def getData(url):
    print2.print2.message('获取中...')
    data = Http.getJson(url)
    print2.print2.message('\r')
    if data == 1:
        return 1
    return data


def getSort():
    try:
        return getData('https://v2.api.dailypics.cn/sort')['result']
    except:
        return 1


def getToday():
    return getData('https://v2.api.dailypics.cn/today')


def getSortList():
    data = getSort()
    if data == 1:
        return 1
    sort = {}
    for v in data:
        sort[v['TID']] = v['T_NAME']
    return sort


def getArchive(TID, page):
    return getData('https://v2.api.dailypics.cn/list/?page=%s&size=15&sort=%s' % (page, TID))


def getWebLink(PID):
    return 'https://www.dailypics.cn/member/id/%s' % PID


def getPicData(PID):
    return getData('https://v2.api.dailypics.cn/member?id=%s' % PID)
