from . import Tujian, Http, print2
import qrcode
import os
import sys


def getImage(pic, path, sort):
    name = sort[pic['TID']]
    title = pic['p_title'].replace(
        '/', '&').replace('\\', '&').replace(':', '')
    date = pic['p_date']
    pid = pic['PID']
    link = pic['local_url']+'?p=0'
    user = pic['username']
    file_path = os.path.join(path, '%s-%s_%s_%s.%s.jpeg' %
                             (date, name, title, pid, user))
    if not os.path.isfile(file_path):
        print('正在获取%s %s %s' % (name, title, link))
        data = Http.downloadB(link, file_path)
        if data == 1:
            print2.error('获取%s %s %s 失败' % (name, title, link))
            return 1
        print2.success('%s 已保存' % file_path)
    else:
        print2.success("%s 已存在" % file_path)
    return 0


def printSort():
    data = Tujian.getSort()
    if data == 1:
        print2.error('加载失败')
        return 1
    for v in data:
        print(v['T_NAME'] + ' -- ' + v['TID'])
    return 0


def getToday(path, sort=None):
    print('获取今日')
    data = Tujian.getToday()
    if data == 1:
        print2.error('加载失败')
        return 1
    if sort == None:
        sort = Tujian.getSortList()
        if sort == 1:
            print2.error('加载失败')
            return 1
    for v in data:
        getImage(v, path, sort)
    print2.success('获取今日 成功')


def getArchive(par, path, sort=None):
    if sort == None:
        sort = Tujian.getSortList()
        if sort == 1:
            print2.error('加载失败')
            return 1
    try:
        TID = par[1]
        TNAME = sort[TID]
    except IndexError:
        print2.error('请输入 TID')
        sys.exit(1)
    except KeyError:
        print2.error('找不到对应的 TID')
        sys.exit(1)
    print('获取 %s (%s)' % (TNAME, TID))
    print('获取第 1 页')
    data = Tujian.getArchive(TID, 1)
    if data == 1:
        print2.error('加载失败')
        return 1
    maxpage = data['maxpage']
    for v in data['result']:
        getImage(v, path, sort)
    print2.success('获取第 1 页 成功')
    for p in range(1, int(maxpage)):
        page = p+1
        print('获取第 %s 页,共 %s 页' % (page, maxpage))
        data = Tujian.getArchive(TID, page)
        if data == 1:
            print2.error('加载失败')
            return 1
        for v in data['result']:
            getImage(v, path, sort)
        print2.success('获取第 %s 页成功' % page)
    print2.success('获取 %s (%s) 成功' % (TNAME, TID))
    return 0


def getAll(path):
    sort = Tujian.getSortList()
    if sort == 1:
        print2.error('加载失败')
        return 1
    getToday(path, sort)
    for k in sort:
        getArchive(['', k], path, sort)
    print2.success('获取所有 成功')


def printQrcode(PID):
    qr = qrcode.QRCode()
    qr.add_data(Tujian.getWebLink(PID))
    qr.print_ascii(invert=True)


def printInfo(data, sort=None):
    if sort == None:
        sort = Tujian.getSortList()
        if sort == 1:
            print2.error('加载失败')
            return 1
    print('「%s」' % data['p_title'])
    print('%s %s %s×%s @%s' % (
        data['p_date'],
        sort[data['TID']],
        data['width'],
        data['height'],
        data['username']
    ))
    print('')
    print(data['p_content'])
    print('')
    print('访问 %s 或扫描二维码查看详情' % Tujian.getWebLink(data['PID']))
    printQrcode(data['PID'])


def printByPID(par):
    sort = Tujian.getSortList()
    if sort == 1:
        print2.error('加载失败')
        return 1
    try:
        PID = par[1]
    except:
        print2.error('请输入 PID')
        sys.exit(1)
    data = Tujian.getPicData(PID)
    if data == 1:
        print2.error('加载失败')
        return 1
    try:
        data['PID']
    except:
        print2.error('没有这张图片')
        sys.exit(1)
    printInfo(data, sort)
