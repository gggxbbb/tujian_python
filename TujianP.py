#coding=utf-8

from urllib import request
from urllib.request import urlretrieve
from urllib import error
import json
import os
import signal

#注意，游标卡尺的单位长度为4
#请使用Python3

def exitTujianP():
    event = input('确认要退出吗?(Y/n)')
    print('')
    if event.lower() == "y": 
        print('再见')
        print('>>>TujianP<<<')
        print('')
        exit()
    elif event.lower() == "n":
        return
    else:
        print('虽然不知道你输入了什么，但一定是想留下的，对吧？')
        return

def exitTujian(signum,frame):
    print('\n')
    print('再见')
    print('>>>TujianP<<<')
    print('')
    exit()

signal.signal(signal.SIGINT,exitTujian)
signal.signal(signal.SIGTERM,exitTujian)

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

dir = './Tujian/'
if not os.path.isdir(dir):
    os.makedirs(dir)

print('>>>Welcone!<<<')

def getImage(name,pic):
    title = pic['p_title'].replace('/','&').replace('\\','&')
    date = pic['p_date']
    pid = pic['PID']
    link = pic['local_url']
    user = pic['username']
    path = './Tujian/%s-%s_%s_%s.%s.jpeg'%(date,name,title,pid,user)
    if not os.path.isfile(path):
        print('正在获取%s %s %s'%(name,title,link))
        if (link.find('i.loli.net') != -1) or (link.find('ooo.0o0.ooo') != -1):
            print('站外图片，跳过')
        else:
            req = request.Request(link, headers=header)
            data = request.urlopen(req).read()
            with open(path, 'wb') as f:
                f.write(data)
                f.close()
                print('%s 已保存'%path)
    else:
        print("%s 已存在"%path)

def getPics(name,tid,page):
    print('获取 %s 第 %s 页'%(name,page))
    reqPicsUrl = request.Request(url='https://api.dpic.dev/list/?page=%s&size=15&sort=%s'%(page,tid),
    headers=header)
    reqPics = request.urlopen(reqPicsUrl)
    dataPics = json.loads(reqPics.read().decode('utf-8'))
    print('获取 %s 第 %s 页原始数据:OK'%(name,page))
    for pic in dataPics["result"]:
        getImage(name,pic)
    print('获取 %s 第 %s 页:OK'%(name,page))
    if (page < dataPics['maxpage']):
        print('%s 共%s页'%(name,dataPics['maxpage']))
        getPics(name,tid,page +1)
    else:
        print('获取 %s :OK'%name)

def getSort():
    print('获取分类')
    reqSortUrl=request.Request(url='https://api.dpic.dev/sort/',
    headers=header)
    reqSort = request.urlopen(reqSortUrl)
    dataSort = reqSort.read().decode('utf-8')
    tujianSort = json.loads(dataSort)
    print('获取分类:OK')
    return tujianSort["result"]

def getAll():
    picSort = getSort()
    for m in picSort:
        sortName = m["T_NAME"]
        sortTID = m["TID"]
        print('获取 %s TID: %s'%(sortName,sortTID))
        getPics(sortName,sortTID,1)

def chooseSort(sort):
    picSort = {}
    print('请选择分类')
    for m in sort:
        sortName = m["T_NAME"]
        sortTID = m["TID"]
        print('>%s'%sortName)
        picSort[sortName] = sortTID
    print('输入 0 退出')
    print('输入 1 返回操作列表')
    iSort = input('输入分类名>')
    if iSort == "0":
        exitTujianP()
    elif iSort == "1":
        return
    else:
        try:
            getPics(iSort,picSort[iSort],1)
        except:
            print('错误 请重试')
            chooseSort(sort)
    

def getPicBySort():
    chooseSort(getSort())

def getToday():
    reqTodayUrl=request.Request(url='https://api.dpic.dev/today/',
    headers=header)
    reqToday = request.urlopen(reqTodayUrl)
    dataToday = reqToday.read().decode('utf-8')
    tujianToday = json.loads(dataToday)
    print('获取今日图片原始数据:OK')
    for pic in tujianToday:
        getImage(pic['T_NAME'],pic)
    print('获取今日图片:OK')
        
def serverTest():
    try:
        print('尝试与服务器建立连接')
        reqTestUrl=request.Request(url='https://api.dpic.dev/',
        headers=header)
        request.urlopen(reqTestUrl)
    except error.HTTPError as err:
        print('服务器已去世 错误信息: %s'%err)
    else:
        print('服务器正常')
        start()

def start():
    print('')
    print('>>>TujianP<<<')
    print('选择操作:')
    print('0.退出')
    print('1.获取全部')
    print('2.获取今日')
    print('3.按分类获取全部')
    print('98.搜索')
    print('99.关于')
    print('100.服务器测试')
    print('')
    event = input('请输入操作前数字>')
    print('')
    if event == "0":
        exitTujianP()
    elif event == '1':
        getAll()
    elif event == '2':
        getToday()
    elif event == '3':
        getPicBySort()
    elif event == '98':
        print(':)请至 AppStore(Apple) 或其它应用商店(Android)下载 Tujian 或其它第三方版本体验此功能和其它高级功能')
    elif event == "99":
        print(':)这是一个使用 Python 编写的，用于获取 Tujian 图片的简易工具')
    elif event == '100':
        serverTest()
    else:
        print('输入错误 请重试')
    start()
        
#start()
serverTest()