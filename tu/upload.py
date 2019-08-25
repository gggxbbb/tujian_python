import yaml
import sys
from . import Http
from . import print2

def uploadPic(pic,name,mail):
    data = {}
    try:
        data['title']=pic['title']
        data['content']=pic['content']
        data['sort']=pic['sort']
    except:
        print2.error('请提供完整的图片信息')
        return 1
    data['user']=name
    data['hz']=mail
    print('正在提交 %s'%pic['title'])
    try:
        path = pic['path']
        print2.print2.message('%s 上传中'%pic['title'])
        data2 = Http.uploadBJSON('https://img.dpic.dev',path)
        if data2 == 1:
            print2.error('\r%s 上传失败'%pic['title'])
            return 1
        if data2['ret'] == True:
            link = 'https://img.dpic.dev/' + data2['info']['md5']
            print2.success('\r上传成功')
        else:
            print2.error(('\r%s 上传失败: '%pic['date'])+data2['info']['message'])
            return 1
    except:
        try:
            link = pic['link']
        except:
            print2.error('请为 %s 提供图片地址或链接'%pic['title'])
    data['url']=link
    print2.print2.message('\n%s 提交中'%pic['title'])
    message = Http.postJSON('https://v2.api.dailypics.cn/tg',data)
    if message == 1:
        print2.success('\r%s 提交失败'%pic['title'])
        return 1
    if message['code'] == 200:
        print2.success('\r%s 提交成功'%pic['title'])
    else:
        print2.error(('\r%s 提交失败: '%pic['title'])+message['msg'])
        return 1

def upoladPics(par):
    try:
        yaml.warnings({'YAMLLoadWarning': False})
        data = yaml.load(open(par[1],encoding='utf-8').read())
    except:
        print2.error('请检查文件!')
        sys.exit(1)
    try:
        name = data['name']
        mail = data['mail']
    except:
        print2.error('请提供用户名及邮箱')
    err = 0
    for v in data['pics']:
        err += uploadPic(v,name,mail)
    print2.success('全部提交完成,共 %s 个,成功 %s 个,失败 %s 个'%(len(data['pics']),len(data['pics']) - err,err))