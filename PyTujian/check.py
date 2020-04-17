import sys

import dhash
from PIL import Image

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from .Tujian import getData
from .tools import printByPID

def dHash(path):
    with Image.open(path) as image:
        row, col = dhash.dhash_row_col(image)
    return dhash.format_hex(row, col)

def check(pars):
    local = dHash(pars[1])
    rData = getData('http://tu.gggxbbb.tk/dhash.json')
    p = []
    for k in rData:
        rValue = rData[k]
        rHash = dict(zip(range(0,len(rValue)),rValue))
        d = 0
        for key in rHash:
            if rHash[key] == local[key]:
                d += 1
        pre = d/len(rValue)
        if pre >= 0.4:
            p.append(['%0.2f'%(pre*100)+'%',k])
    print('疑似撞车图片:')
    if len(p) == 0:
        print('无')
    for v in p:
        printByPID([None,v[1]])
        print('相似度:'+v[0])
        print('-'*8)



