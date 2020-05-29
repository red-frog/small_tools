#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random

import requests
import json

import time
import execjs


common_translate_key = {'0-2': '0-2', '3-5': '3-5', '6-13': '6-13', '14-18': '14 -18', '19-40': '19 -40',
                        '41-60': '41 -60', '60+': '60 +', 'Very rare': '非常罕见', 'Rare': '稀有',
                        'Common': '常见', 'Very common': '很常见', 'Never': '从不', 'Extremely rare': '非常罕见',
                        'Pain areas: ': '疼痛部位：', 'Gastrointestinal: ': '胃肠道：', 'Whole body: ': '全身：',
                        'Also common: ': '也常见于：', 'Mood: ': '心情：', 'Psychological: ': '心理：',
                        'Behavioral: ': '行为：', 'Cognitive: ': '认知：', 'Weight: ': '体重：',
                        'Neck: ': '脖子：', 'Cough: ': '咳嗽：', 'Mouth: ': '口腔：', 'Joints: ': '关节：',
                        'Hand: ': '手：', 'Heart: ': '心脏：', 'Sleep: ': '睡眠：', 'Pain types: ': '疼痛类型：',
                        'Pain circumstances: ': '疼痛情况：', 'Urinary: ': '尿液：', 'Sensory: ': '感觉：',
                        'Menstrual: ': '月经：', 'Skin: ': '皮肤：', 'Devices': '设备', 'Eyes: ': '眼睛：',
                        'Visual: ': '视觉：', 'Speech: ': '演讲：', 'Facial: ': '面部：', 'Limbs: ': '四肢：',
                        'Hair: ': '头发：', 'Throat: ': '喉咙：', 'Groin: ': '腹股沟：',
                        'Respiratory: ': '呼吸道：', 'Common symptoms: ': '常见症状：', 'Nasal: ': '鼻腔：',
                        'Headache: ': '头痛：', 'Tremor: ': '震颤：', 'Sexual: ': '性：',
                        'Developmental: ': '发育：', 'Abdominal: ': '腹部：', 'Ears: ': '耳朵：',
                        'Head: ': '头：', 'Anal: ': '肛门：', 'Breast: ': '乳房：', 'Arm: ': '手臂：',
                        'Nails: ': '钉子：', 'Chest: ': '胸部：', 'Medications': '药物',
                        'Medical procedure': '医疗程序', 'Surgery': '手术', 'Supportive care': '支持治疗',
                        'Specialists': '专家', 'Therapies': '治疗', 'Self-care': '自我治疗',
                        'Males': '男性', 'Females': '女性', 'Ask a doctor': '咨询医生',
                        'Preventative': '预防', 'Muscular: ': '肌肉：'}


class Py4Js(object):
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
        };      
        function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
      } 
     """)

    def get_tk(self, text):
        return self.ctx.call("TL", text)


def build_url(text, tk):
    base_url = 'https://translate.google.cn/translate_a/single'
    base_url += '?client=t&'
    base_url += 's1=auto&'
    base_url += 't1=zh-CN&'
    base_url += 'h1=zh-CN&'
    base_url += 'dt=at&'
    base_url += 'dt=bd&'
    base_url += 'dt=ex&'
    base_url += 'dt=ld&'
    base_url += 'dt=md&'
    base_url += 'dt=qca&'
    base_url += 'dt=rw&'
    base_url += 'dt=rm&'
    base_url += 'dt=ss&'
    base_url += 'dt=t&'
    base_url += 'ie=UTF-8&'
    base_url += 'oe=UTF-8&'
    base_url += 'otf=1&'
    base_url += 'pc=1&'
    base_url += 'ssel=0&'
    base_url += 'tsel=0&'
    base_url += 'kc=2&'
    base_url += 'tk='+str(tk)+'&'
    base_url += 'q='+text
    return base_url


def translate(text):
    js = Py4Js()
    header = {
        'authority': 'translate.google.cn',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data': 'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
        }
    try:
        if text in common_translate_key.keys():
            return common_translate_key[text]
        url = build_url(text, js.get_tk(text))
        if text not in ['60+', 'drug_name', 'medication_desc']:
            r = requests.get(url=url, headers=header)
            result = json.loads(r.text)
            response = ''
            if result[7]:
                # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
                try:
                    correct_text = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                    print(correct_text)
                    correct_url = build_url(correct_text, js.get_tk(correct_text))
                    correct_resp = requests.get(correct_url)
                    new_result = json.loads(correct_resp.text)
                    response = new_result[0][0][0]
                    print('correct result 1')
                except Exception as e:
                    print(e, '{} tranlate error'.format(text))
                    response = result[0][0][0]
            else:
                response = result[0][0][0]
            time.sleep(random.randint(1, 4))
            if response:
                return response
        else:
            return text
    except Exception as e:
        print(e, '{} tranlata error 2'.format(text))


if __name__ == '__main__':
    # config_socket()
    resp = translate('60+')
    print(resp)
    print(type(resp))