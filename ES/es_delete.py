
from elasticsearch import Elasticsearch

ES_HOST = 'http:localhost:9200'
es_client = Elasticsearch(hosts=ES_HOST)
print es_client.info()


def delete_from_es(itemid):
    try:
        delete_query = {"query": {"match": {"itemid": itemid}}}
        result = es_client.delete_by_query(index='index', doc_type='doc_type', body=delete_query)
        print result
    except Exception as e:
        print e
        with open('./record.txt', 'a') as f:
            f.write(str(itemid))
            f.write('\n')
# print('hello world')


if __name__ == '__main__':
    for i in range(1334438, 1424438, 1):
        delete_from_es(itemid=i)
    # for i in range(1, 9, 2):
    #     print i
    #     with open('./record.txt', 'a') as f:
    #         f.write(str(i))
    #         f.write('\n')

    # 1334438
    # end 1424438

