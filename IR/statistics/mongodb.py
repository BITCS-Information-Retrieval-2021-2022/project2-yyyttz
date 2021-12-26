from typing import List
import pymongo
import json
import random
import time

host = '127.0.0.1'
port = 28887
username = 'scholar'
passwd = 'r4u30dYkgeqVdlaR'


class MongoProcess:
    def __init__(
        self,
        url='mongodb://{}:{}@{}:{}'.format(username, passwd, host, port),
        db='scholar',
        collection='a_researcher'
    ):
        client = pymongo.MongoClient(url)
        self.db = client[db]
        # self.db.authenticate(username, passwd)
        self.collection = self.db[collection]

        if db not in client.list_database_names():
            print('The database dosen\'t exist.')
        if collection not in self.db.list_collection_names():
            print('The collection dosen\'t exist.')

    def select(self, filter={}, projection={'_id': 0}, skip=0, limit=1000, sort=[]) -> List:
        result = self.collection.find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort)

        return result

    def select_one(self, filter={}, projection={'_id': 0}) -> List:
        result = self.collection.find_one(filter=filter, projection=projection)

        return result

    def delete(self, filter={}) -> int:
        result = self.collection.delete_many(filter=filter)

        return result.deleted_count

    def insert(self, data) -> List:
        ids = self.collection.insert_many(data)

        return ids

    def count(self) -> int:
        return self.collection.find().count()

    def ratio_coverage(self):
        example = self.select_one(projection={'_id': 0})
        result = {}
        for item in example.keys():
            result[item] = 0

        sample = self.select(projection={'_id': 0}, limit=0)
        i = 1
        for doc in sample:
            print('process {}st data'.format(i))
            i += 1
            for item in doc.keys():
                if doc[item] is not None:
                    if (type(doc[item]) == str or type(doc[item]) == List) and len(doc[item]) == 0:
                        continue
                    result[item] += 1

        count = self.count()
        for item in example.keys():
            result[item] /= count

        return result

    def search_by_id(self, id):
        db_query = {"id": id}
        res = self.collection.find_one(db_query, projection={'_id': 0})
        return res

    def search_by_id_list(self, id_list):
        res = []
        for id in id_list:
            res.append(self.search_by_id(id))
        return res


def test():
    start = time.time()
    m = MongoProcess(collection='a_researcher')
    sample = m.select(projection={'_id': 0}, limit=0)
    count = 0

    for doc in sample:
        count += 1
        if(count == 1000):
            break
        print('正在处理第{}个数据'.format(count))
    stop = time.time()
    print("时间差:{}".format(stop - start))


def getData(col='a_paper', begin=0, num=500):
    m = MongoProcess(collection=col)
    sample = m.select(projection={'_id': 0}, skip=begin, limit=num)
    data = [doc for doc in sample]

    return data


if __name__ == '__main__':
    getData()
