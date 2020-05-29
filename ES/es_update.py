#!/usr/bin/env python
# -*- coding:utf-8 -*-

import elasticsearch
import json

ES_Host = 'http://localhostt:9200'
es_client = elasticsearch.Elasticsearch(hosts=ES_Host)


def update_by_body(index, id, fields):
    """

    :param index: es index
    :param id: es id
    :param fields: {key1:value1,key2:value2}
    :return:
    """
    body = {
        "doc": {
        }
    }
    for field in fields:
        if not fields[field]:
            continue
        body["doc"][field] = fields[field]
    res = es_client.update(index=index, doc_type=index, id=id, body=body)
    if res["_shards"]["successful"]:
        return True
    else:
        return False


def read_qb_txt():
    with open('./qb_code.txt', 'r') as f:
        for i in f.readlines():
            record_list = json.loads(i)
            print(type(record_list))
            if record_list[1]:
                resp = update_by_body(index='oafile', id=record_list[0], fields={'itemid': record_list[0], 'code': record_list[1]})
                if not resp:
                    print record_list
            break


if __name__ == '__main__':
    read_qb_txt()
