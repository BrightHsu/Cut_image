#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    @Time    : 2020/6/12 14:35
    @Author  : David Ben
    @FileName: test.py
    @Email: hsudavid@163.com
    @Software: PyCharm
"""


from PIL import Image
from functools import wraps
import os
import json
import time


def log(text=None):
    if isinstance(text, str):
        def wrapper(fun):
            @wraps(fun)
            def inner_wrapper(*args, **kwargs):
                print(text, fun.__name__)
                new = fun(*args, **kwargs)
                return new
            return inner_wrapper
        return wrapper
    else:
        @wraps(text)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            new = text(*args, **kwargs)
            t2 = time.time()
            name = text.__name__
            print(name, '运行', round((t2 - t1) * 1000), 'ms')
            return new
        return wrapper


def data_from_json(json_file):
    with open(json_file, 'rb') as f:
        data = json.load(f)

    for i in data['res']:
        image_data = {}
        image_data['name'] = i.strip()
        image_data['x'] = data['res'][i]['pos'][0]
        image_data['y'] = data['res'][i]['pos'][1]
        image_data['w'] = data['res'][i]['size'][0]
        image_data['h'] = data['res'][i]['size'][1]
        yield image_data


@log
def cut_image(save_dir, json_file, image_file):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    image = Image.open(image_file)
    """:type:Image.Image"""

    image_data = data_from_json(json_file)

    for i in image_data:
        name = i['name']
        x = i['x']
        y = i['y']
        w = i['w']
        h = i['h']

        box = (x, y, w + x, h + y)

        new_image = image.crop(box)

        if os.path.splitext(image_file)[1] == '.png':
            new_image.save(os.path.join(save_dir, name + '.png'))
        else:
            new_image.save(os.path.join(save_dir, name + '.jpg'))


if __name__ == "__main__":
    # 绝对路径
    abspath = r"C:\Users\Administrator\Desktop\cut_image\demo"
    name_list = [
        os.path.splitext(i)[0] for i in os.listdir(abspath) if os.path.isfile(
            os.path.join(
                abspath,
                i)) and os.path.splitext(i)[1] == '.json']
    # print(name_list)  打印目录名称

    for i in name_list:
        save_dir = os.path.join(abspath, i)
        json_file = os.path.join(abspath, i + '.json')
        png_file = os.path.join(abspath, i + '.png')
        jpg_file = os.path.join(abspath, i + '.jpg')

        if os.path.exists(json_file):
            if os.path.exists(png_file):
                try:
                    cut_image(save_dir, json_file, png_file)
                except Exception as e:
                    print(e, 'png解析出错')
            if os.path.exists(jpg_file):
                try:
                    cut_image(save_dir, json_file, jpg_file)
                except Exception as e:
                    print(e, 'jpg解析出错')
