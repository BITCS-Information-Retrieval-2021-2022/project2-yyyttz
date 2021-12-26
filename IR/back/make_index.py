import os
import csv
import tqdm
import argparse
from elasticsearch import Elasticsearch, helpers
import mongodb


def make_index(index_name, list, total=100_0000):
    # extract
    properties = {}
    for i in list:
        properties[i] = {
            'type': 'text'
        }

    # region 创建索引
    # if not es.indices.exists(index=index_name):
    try:
        es_index = {
            "mappings": {
                "properties": properties
            }
        }

        es.indices.create(index=index_name, body=es_index, ignore=[400])
        chunk_size = 500
        print("过程中可以通过Ctrl+C暂停暂停索引，之前的数据可用")
        with tqdm.tqdm(total=total) as pbar:
            for start_idx in range(779500, total, chunk_size):
                data = mongodb.getData(index_name, start_idx, chunk_size)

                bulk_data = []
                for idx, item in enumerate(data):
                    _source = {}
                    for i in list:
                        _source[i] = item[i] if item[i] else "None"

                    bulk_data.append({
                        "_index": index_name,
                        "_id": idx + start_idx,
                        "_source": _source
                    })

                helpers.bulk(es, bulk_data)
                pbar.update(chunk_size)
    except Exception as e:
        print(e)
        print("索引过程中发生错误，稍后请进行检查\n\n")
    # endregion


if __name__ == "__main__":
    es = Elasticsearch()
    if not es.ping():
        raise Exception("请打开ES")

    index_name = 'a_paper'
    list = ['id', 'title']
    make_index(index_name, list, total=150_0000)
