#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from PyInstaller.__main__ import run
#  -F:打包成一个EXE文件 D,打包成一个文件夹
#  -w:不带console输出控制台，window窗体格式
#  --paths：依赖包路径
#  --icon：图标
#  --noupx：不用upx压缩
#  --clean：清理掉临时文件


#十分重要！！！！！！！！！！！！
#exe必须与两个jar和数据库文件放到一起才能够正常运行


if __name__ == '__main__':
    opts = ['-D',
            #'--paths=D:\\Program Files\\Python\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            #'--paths=D:\\Program Files\\Python\\Lib\\site-packages\\jpype',
            #'--paths=D:\\Program Files\\Python\\Lib\\site-packages\\numpy'
            #'--noupx',
            #'--clean',
            #'--hidden-import=numpy',
            'main.py']
    run(opts)
