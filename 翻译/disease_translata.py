#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
author:zhao
date: 2018.10.23
"""
import datetime
import json
import random

# from googletrans import Translator
from lxml import etree
import time
import requests
import pymongo
from small_tools.google_translate_1 import translate


uri = 'mongodb://username:password@host:port/db'
mongo_client = pymongo.MongoClient(uri)


def config_socket():

    import socket
    import socks
    SOCKS5_PROXY_HOST = '127.0.0.1'
    SOCKS5_PROXY_PORT = 3005  # socks 代理本地端口
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
    socket.socket = socks.socksocket

    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    socket.getaddrinfo = getaddrinfo


untrans_list = ['name', 'content', 'disease_name', 'disease_alias', 'disease_image', 'disease_description',
                'disease_level', 'disease_incidence', 'treatment_advice', 'disease_cause', 'disease_symptom',
                'disease_treatment', 'age_distribution', 'related_condition', 'diagnostic_method', 'experience',
                'care_method', 'treatment_desc']


# translator = Translator(service_urls=['translate.google.com'])


# def translate(text):
#     config_socket()
#     info_zh = translator.translate(text, src='en', dest='zh-cn').text
#     time.sleep(random.randint(3, 5))
#     return info_zh


def insert(disease_name, item):
    """item:json"""
    try:
        db = mongo_client.zhiu_disease
        # 获取集合对象(英文)
        collection = db.diseases_zh
        item = dict(item)
        new_item = dict(name=disease_name, content=item)
        collection.insert(new_item)
        print(datetime.datetime.now(), '{} insert mongo success'.format(disease_name))
        return True
    except Exception as e:
        print(datetime.datetime.now(), e)
        return False


def parse_content(content):
    content_zh_dict = {}
    for k, v in content.items():
        if k not in untrans_list:
            k = translate(text=k)
        if type(v) == list:
            new_list = list()
            for i in v:
                new_list.append(translate(text=i))
            content_zh_dict[k] = new_list
        elif type(v) == dict:
            content_zh_dict[k] = parse_content(content=v)
        else:
            content_zh_dict[k] = translate(v) if v else None
    return content_zh_dict


def handle_disease_info(disease_name, content):
    config_socket()
    tem_image = content.pop('disease_image')
    content.pop('disease_name')
    disease_name_zh = translate(text=disease_name)
    print('here1')
    content_zh_dict = parse_content(content=content)
    print('here2')
    content_zh_dict['disease_name'] = disease_name_zh
    content_zh_dict['disease_image'] = tem_image
    # # 写入es
    # insert_es(index=disease_name_zh, body=disease_data_zh_dict)
    # 写入mongo
    resp = insert(disease_name=disease_name_zh, item=content_zh_dict)
    if resp:
        with open('been_translate.txt', 'a') as f:
            f.write(disease_name + ' : ' + disease_name_zh)
            f.write('\n')
    else:
        with open('record_error_msg.txt', 'a') as f:
            f.write(str(content_zh_dict))
            f.write('\n')
            f.write(disease_name)
            f.write('\n')


def conn_mongodb():
    try:
        # uri = 'mongodb://zhiu_disease:fftechs.cn@192.168.32.35:27017/zhiu_disease'
        # # with pymongo.MongoClient(uri) as mongo_client:
        # mongo_client = pymongo.MongoClient(uri)
        db = mongo_client.zhiu_disease
        # 获取集合对象(英文)
        disease_collection = db.diseases_en
        count = 0
        for data in disease_collection.find().sort("_id", -1):
            disease_name = data['name']
            print(disease_name)
            count += 1
            if count == 170:
                break
            if disease_name in been_translate_list:
                continue
            content = data['content']
            handle_disease_info(disease_name=disease_name, content=content)
        print('translate end')
        mongo_client.close()
    except Exception as e:
        print(datetime.datetime.now(), e)


if __name__ == '__main__':
    disease_dict = dict()
    with open('been_translate.txt', 'r') as f:
        for i in f.readlines():
            tem_list = i.split(' : ')
            disease_dict[tem_list[1].strip()] = tem_list[0].strip()
    name_zh_keys_list = list(disease_dict.keys())
    been_translate_list = list(disease_dict.values())
    conn_mongodb()


