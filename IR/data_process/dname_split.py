'''
重名区分的算法实现
'''
from typing import List
import pymongo
import json
import random

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

    def select(self, filter={}, projection={'_id': 0}, limit=1000, sort=[]) -> List:
        result = self.collection.find(filter=filter, projection=projection, limit=limit, sort=sort)

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


def combine_researcher():
    last_mongo = MongoProcess(collection='researcher')
    new_mongo = MongoProcess(collection='a_researcher')
    error_doc = []

    last_researchers = last_mongo.select(projection={'_id': 0}, limit=0)

    count = 1
    for doc in last_researchers:
        print('正在处理第{}个数据'.format(count))
        count += 1
        new_mongo.insert([doc])

    with open('error_doc.json', 'w', encoding='UTF-8') as f:
        json.dump(error_doc, f)


def delete_null_id():
    newMongo = MongoProcess()
    filter = {'id': None}
    newMongo.delete(filter)


def remove_duplicate_id():
    newMongo = MongoProcess(collection='a_researcher')
    projection = {'_id': 1, 'id': 1}
    result = newMongo.select(filter={}, projection=projection, limit=0, sort=[('id', 1)])

    last = None
    count = 1
    for i in result:
        if i['id'] == last:
            newMongo.delete({'_id': i['_id']})
            continue
        last = i['id']
        print('正在处理第{}个数据'.format(count))
        count += 1


def build_dataset():
    paperMongo = MongoProcess(collection='a_paper')
    full_datas = paperMongo.select(projection={'_id': 0, 'title': 1, 'authors': 1}, limit=0)

    count = 0
    data = []
    for doc in full_datas:
        print('正在处理第{}个数据'.format(count))
        count += 1

        if count % 50000 == 1:
            with open('data_{}.json'.format(count // 50000), 'w', encoding='UTF-8') as f:
                json.dump(data, f)
            data = []
        data.append(doc)


def count_data():
    paperMongo = MongoProcess(collection='a_paper')
    researcherMongo = MongoProcess(collection='a_researcher')
    full_datas = paperMongo.select(projection={'_id': 0, 'authors': 1}, limit=0)

    id_count, no_id_count, id_inre_count = 0, 0, 0
    count = 1
    for doc in full_datas:
        print('正在处理第{}个数据'.format(count))
        count += 1

        if doc['authors'] is None or len(doc['authors']) == 0:
            continue

        for i in doc['authors']:
            if 'id' in i.keys():
                id_count += 1
                result = researcherMongo.select_one(filter={'id': i['id']})
                if result is not None:
                    id_inre_count += 1
            else:
                no_id_count += 1

    with open('count_data.txt', 'a', encoding='utf-8') as f:
        line1 = 'id_count = {}; no_id_count = {}; total = {}\n'.format(id_count, no_id_count, id_count + no_id_count)
        line2 = 'there are {} id in a_researcher, except {}\n'.format(id_inre_count, id_count - id_inre_count)
        f.write(line1 + line2)


def extract_data():
    paperMongo = MongoProcess(collection='a_paper')
    researcherMongo = MongoProcess(collection='a_researcher')
    full_datas = paperMongo.select(projection={'_id': 0, 'title': 1, 'authors': 1}, limit=0)

    # id_count, no_id_count, id_inre_count = 0, 0, 0
    count = 1
    id_list = set()
    for doc in full_datas:
        print('正在处理第{}个数据'.format(count))
        count += 1

        if doc['authors'] is None or len(doc['authors']) == 0 or doc['title'] is None:
            continue

        flag = 0
        subline = ''
        authors = [i for i in doc['authors'] if 'id' in i.keys() and 'name' in i.keys()]
        if len(authors) < 2:
            continue

        for i in authors:
            if i['id'] in id_list:
                result = researcherMongo.select_one(filter={'id': i['id']})
                if result is None:
                    continue
                flag += 1
                subline = '\t\t\t\t\t' + i['id'] + '\t\t' + i['name']
            elif len(id_list) < 10000:
                result = researcherMongo.select_one(filter={'id': i['id']})
                if result is None:
                    continue
                id_list.add(i['id'])
                flag += 1
                subline = '\t\t\t\t\t' + i['id'] + '\t\t' + i['name']

        if flag >= 2:
            line = doc['title'] + subline + '\n'
            with open('full_data.txt', 'a', encoding='UTF-8') as f:
                f.write(line)

    for id in id_list:
        with open('id_list.txt', 'a', encoding='utf-8') as f:
            f.write(id + '\n')


def build_vetex_list():
    researcherMongo = MongoProcess(collection='a_researcher')

    fw = open('id_author.txt', 'a', encoding='utf-8')
    with open('id_list.txt', 'r', encoding='utf-8') as f:
        x = f.readline()
        while x != '':
            id = x.replace('\n', '')
            result = researcherMongo.select_one(filter={'id': id}, projection={'_id': 0, 'name': 1})
            print(result)
            fw.write(id + '\t\t\t' + result['name'] + '\n')
            x = f.readline()
    fw.close()


num_epoch = 5
num_train = 15000


def build_graph():
    vetex_index = {}
    id_vetex = {}
    with open('id_author.txt', 'r', encoding='utf-8') as f:
        count = 0
        line = f.readline().replace('\n', '')
        while line != '':
            id, name = line.split('\t\t\t')
            vetex_index[name] = {'id': id, 'index': count}
            id_vetex[id] = name
            count += 1
            line = f.readline().replace('\n', '')

    full_data = []
    with open('full_data.txt', 'r', encoding='utf-8') as f:
        line = f.readline().replace('\n', '')
        while line != '':
            term = line.split('\t\t\t\t\t')
            title = term[0]
            try:
                name_id = [{'id': i.split('\t\t')[0], 'name': i.split('\t\t')[1]} for i in term[1:]]
                x = {'title': title, 'authors': name_id}
                full_data.append(x)
            except Exception:
                pass
            finally:
                line = f.readline().replace('\n', '')

    num_vetex = len(id_vetex.keys())
    for epoch in range(1, num_epoch + 1):
        random.shuffle(full_data)
        train_data = full_data[:num_train]
        test_data = full_data[num_train:]
        graph = [[0 for i in range(num_vetex)] for j in range(num_vetex)]

        for i in train_data:
            ids = [j['id'] for j in i['authors']]
            length = len(ids)
            for x in range(length):
                for y in range(x, length):
                    id_x = vetex_index[id_vetex[ids[x]]]['index']
                    id_y = vetex_index[id_vetex[ids[y]]]['index']
                    graph[id_x][id_y] += 1
                    graph[id_y][id_x] += 1

        acc = 0
        for i in test_data:
            names = [j['name'] for j in i['authors']]
            id_labels = [j['id'] for j in i['authors']]
            id_result = [0 for i in range(len(names))]
            count = 0
            for k in range(len(names)):
                name = names[k]
                if name in vetex_index.keys():
                    id_result[k] = vetex_index[name]['id']
                else:
                    pass

                if id_labels[k] == id_result[k]:
                    count += 1
            acc += float(count) / len(names)

        acc = acc / len(test_data)

        with open('result.txt', 'a', encoding='utf-8') as f:
            line = 'epoch:{}; acc:{}\n'.format(epoch, acc)
            print(line)
            f.write(line)


def main():
    paperMongo = MongoProcess(collection='a_paper')
    full_datas = paperMongo.select(projection={'_id': 0, 'authors': 1}, limit=0)

    count = 0
    right = 0
    for doc in full_datas:
        id_list = []
        name_list = []
        # print('正在处理第{}个数据'.format(count))

        if doc['authors'] is None or len(doc['authors']) == 0:
            continue

        for i in doc['authors']:
            if 'id' in i.keys() and 'name' in i.keys():
                id_list.append(i['id'])
                name_list.append(i['name'])

        if len(id_list) > 1:
            for i in range(0, len(id_list)):
                for j in range(i, len(id_list)):
                    try:
                        mongo = MongoProcess(collection='author_name')
                        idx_list = mongo.select_one(filter={'name': name_list[i]})
                        idy_list = mongo.select_one(filter={'name': name_list[j]})

                        print('new', len(idx_list), len(idy_list))
                        max = 0
                        id11 = ''
                        id22 = ''
                        for id1 in idx_list['ids']:
                            for id2 in idy_list['ids']:
                                print(id1, id2)
                                mongo1 = MongoProcess(collection='author_relation')
                                filter = {
                                    '$or': [
                                        {'author_x': id1, 'author_y': id2},
                                        {'author_x': id2, 'author_y': id1}
                                    ]
                                }
                                edge = mongo1.select_one(filter=filter)
                                if edge > max:
                                    id11 = id1
                                    id22 = id2
                                    max = edge

                            # evalution
                            if id11 == id_list[i] and id22 == id_list[j]:
                                count += 1
                                right += 1
                            elif id22 == id_list[i] and id11 == id_list[j]:
                                count += 1
                                right += 1
                            else:
                                count += 1

                            print('count:', count, 'right:', right)
                    except Exception:
                        pass

    with open('d_name.txt', 'r', encoding='utf-8') as fw:
        fw.write('count: {}, right: {}'.format(count, right))


if __name__ == '__main__':
    main()
