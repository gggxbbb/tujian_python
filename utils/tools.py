from . import Tujian,Http,print2
import os,sys

def getImage(pic,path,sort):
    name = sort[pic['TID']]
    title = pic['p_title'].replace('/','&').replace('\\','&')
    date = pic['p_date']
    pid = pic['PID']
    link = pic['local_url']+'?p=0'
    user = pic['username']
    file_path = os.path.join(path,'%s-%s_%s_%s.%s.jpeg'%(date,name,title,pid,user))
    if not os.path.isfile(file_path):
        print('正在获取%s %s %s'%(name,title,link))
        Http.downloadB(link,file_path)
        print2.success('%s 已保存'%file_path)
    else:
        print2.success("%s 已存在"%file_path)

def printSort():
    data = Tujian.getSort()
    for v in data:
        print(v['T_NAME'] + ' -- ' + v['TID'])

def getToday(path,sort=None):
    print('获取今日')
    data = Tujian.getToday()
    if sort==None:
        sort = Tujian.getSortList()
    for v in data:
        getImage(v,path,sort)
    print2.success('获取今日 成功')

def getArchive(par,path,sort=None):
    if sort==None:
        sort = Tujian.getSortList()
    try:
        TID = par[1]
        TNAME = sort[TID]
    except IndexError:
        print2.error('请输入 TID')
        sys.exit(1)
    except KeyError:
        print2.error('找不到对应的 TID')
        sys.exit(1)
    print('获取 %s (%s)'%(TNAME,TID))
    print('获取第 1 页')
    data = Tujian.getArchive(TID,1)
    maxpage = data['maxpage']
    for v in data['result']:
        getImage(v,path,sort)
    print2.success('获取第 1 页 成功')
    for p in range(1,int(maxpage)):
        page = p+1
        print('获取第 %s 页,共 %s 页'%(page,maxpage))
        data = Tujian.getArchive(TID,page)
        for v in data['result']:
            getImage(v,path,sort)
        print2.success('获取第 %s 页成功'%page)
    print2.success('获取 %s (%s) 成功'%(TNAME,TID))

def getAll(path):
    sort = Tujian.getSortList()
    getToday(path,sort)
    for k in sort:
        getArchive(['',k],path,sort)
