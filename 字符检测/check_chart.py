#!/usr/bin/env python
# -*- coding:utf-8 -*-

import chardet

with open('39江山市亿有限公司.txt', 'rb') as f:
    data = f.read()
    print(chardet.detect(data))
    with open('test.txt', 'wb') as f:
        f.write(data)

with open('1.txt', 'rb') as f:
    data = f.read()
    print(chardet.detect(data))

# print(chardet.detect(b'Hello, world!'))
# print(chardet.detect())
