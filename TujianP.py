#coding=utf-8

from urllib import request
from urllib.request import urlretrieve
from urllib import error
from urllib import parse
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
TID_TNAME={'4ac1c07f-a9f7-11e8-a8ea-0202761b0892':'插画','5398f27b-a9f7-11e8-a8ea-0202761b0892':'杂烩','e5771003-b4ed-11e8-a8ea-0202761b0892':'电脑壁纸'}

dir = './Tujian/'
if not os.path.isdir(dir):
    os.makedirs(dir)

print('>>>Welcone!<<<')

def getImage(pic):
    name = TID_TNAME[pic['TID']]
    title = pic['p_title'].replace('/','&').replace('\\','&')
    date = pic['p_date']
    pid = pic['PID']
    link = pic['local_url']
    user = pic['username']
    path = './Tujian/%s-%s_%s_%s.%s.jpeg'%(date,name,title,pid,user)
    if not os.path.isfile(path):
        print('正在获取%s %s %s'%(name,title,link))
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
        getImage(pic)
    print('获取 %s 第 %s 页:OK'%(name,page))
    if (page < dataPics['maxpage']):
        print('%s 共%s页'%(name,dataPics['maxpage']))
        getPics(name,tid,page +1)
    else:
        print('获取 %s :OK'%name)

def getSort():
    # print('获取分类')
    # reqSortUrl=request.Request(url='https://api.dpic.dev/sort/',
    # headers=header)
    # reqSort = request.urlopen(reqSortUrl)
    # dataSort = reqSort.read().decode('utf-8')
    # tujianSort = json.loads(dataSort)
    # print('获取分类:OK')
    # return tujianSort["result"]
    return [{"TID":"4ac1c07f-a9f7-11e8-a8ea-0202761b0892","T_NAME":"插画"},{"TID":"5398f27b-a9f7-11e8-a8ea-0202761b0892","T_NAME":"杂烩"},{"TID":"e5771003-b4ed-11e8-a8ea-0202761b0892","T_NAME":"电脑壁纸"}]

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
    print('输入 1 返回上一级')
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
        getImage(pic)
    print('获取今日图片:OK')

def getPicByID(pics):
    print('输入 0 返回上一级')
    id = input("输入序号>")
    if id == '0':
        return
    try:
        id = int(id)
        pic = pics[id-1]
        getImage(pic)
    except:
        print('输入错误 请重试')
        print('')
        getPicByID(pics)

def searchPic():
    info = parse.quote(input('输入关键字>'))
    reqSearUrl = request.Request(url='https://api.dpic.dev/search/s/%s'%info,
    headers=header)
    reqSear = request.urlopen(reqSearUrl)
    dataSear = json.loads(reqSear.read().decode('utf-8'))
    tujianSear = dataSear['result']
    print('搜索结果(共 %s 个):'%dataSear['total'])
    print('')
    for info in enumerate(tujianSear):
        pic = info[1]
        print('%s. %s\n%s\n'%(info[0]+1,pic['p_title'],pic['p_content']))
    getPicByID(tujianSear)


def serverTest():
    try:
        print('尝试与服务器建立连接')
        reqTestUrl=request.Request(url='https://api.dpic.dev/',
        headers=header)
        request.urlopen(reqTestUrl)
    except error.HTTPError as err:
        print('服务器已去世 错误信息: %s'%err)
        exit()
    else:
        print('服务器正常')

def start():
    print('')
    print('>>>TujianP<<<')
    print('选择操作:')
    print('0. 退出')
    print('1. 获取全部')
    print('2. 获取今日')
    print('3. 按分类获取全部')
    print('4. 搜索')
    print('99. 关于')
    print('100. 服务器测试')
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
    elif event == '4':
        searchPic()
    elif event == '98':
        print(':)请至 AppStore(Apple) 或其它应用商店(Android)下载 Tujian 或其它第三方版本体验此功能和其它高级功能')
    elif event == "99":
        print(':)这是一个使用 Python 编写的，用于获取 Tujian 图片的简易工具')
    elif event == '100':
        serverTest()
    else:
        print('输入错误 请重试')
    start()
        
serverTest()
start()
