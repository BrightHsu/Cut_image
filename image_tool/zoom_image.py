#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    @Time    : 2020/6/12 13:05
    @Author  : David Ben
    @FileName: test.py
    @Email: hsudavid@163.com
    @Software: PyCharm
"""


import os
from PIL import Image
import functools
import time


def log(text=None):
    if isinstance(text, str):
        def wrapper(func):
            @functools.wraps(func)
            def inner_wrapper(*args, **kw):
                print(text)
                print('start:{}'.format(func.__name__))
                t1 = time.time()
                data = func(*args, *kw)
                t2 = time.time()
                print('end:{}'.format(func.__name__))
                print('time {}ms'.format((t2 - t1) * 1000))
                return data
            return inner_wrapper
        return wrapper
    else:
        @functools.wraps(text)
        def wrapper(*args, **kw):
            print('start:{}'.format(text.__name__))
            t1 = time.time()
            data = text(*args, *kw)
            t2 = time.time()
            print('end:{}'.format(text.__name__))
            print('time{}ms'.format((t2 - t1) * 1000))
            return data
        return wrapper


@log
def zoom_image(save_file, png_file, scale):
    old_png = Image.open(png_file)
    """:type:Image.Image"""

    x, y = old_png.size

    x = round(x * scale)
    y = round(y * scale)
    new_png = old_png.resize((x, y), Image.ANTIALIAS)
    new_png.save(os.path.join(save_file, os.path.split(png_file)[1]))


if __name__ == '__main__':
    abspath = r'C:\Users\Administrator\Desktop\cut_image\demo'
    scale = 2  # 缩放比例
    save_file = os.path.join(abspath, 'scale{}'.format(scale))

    if os.path.exists(abspath):
        if not os.path.exists(save_file):
            os.mkdir(save_file)

        png_file = [i for i in os.listdir(abspath) if os.path.isfile(
            os.path.join(abspath, i)) and os.path.splitext(i)[1] == '.png']

        # print(png_file)
        for i in png_file:
            png_file = os.path.join(abspath, i)
            try:
                zoom_image(save_file, png_file, scale)
            except Exception as e:
                print(e)
