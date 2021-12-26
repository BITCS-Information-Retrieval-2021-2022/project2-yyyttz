'''
数据库统计 for 验收
'''
from mongodb import MongoProcess
import json
import numpy as np

table_data_file = 'table_data.txt'
paper_author_file = 'paper_author_data.txt'
author_id_file = 'author_id.txt'
id_name_file = 'id_name.json'


def data_count():
    cols = [
        'author_relation',
        're_paper',
        'tag_author',
        'author_name',
        'a_researcher',
        'a_paper',
        'aminer_paper',
        'aminer_researcher',
        'paper',
        'researcher',
        'semantic_paper',
        'semantic_researcher'
    ]

    fw = open(table_data_file, 'a', encoding='UTF-8')
    for col in cols:
        mongo = MongoProcess(collection=col)
        ratio_coverage = mongo.ratio_coverage()
        count = mongo.count()

        fw.write(col + '\n')
        fw.write('count: {}\n'.format(count))
        for i in ratio_coverage.keys():
            fw.write('{}: {:.4f}\n'.format(i, ratio_coverage[i]))
        fw.write('-------------\n\n')

    fw.close()


def author_number(col):
    mongo = MongoProcess(collection=col)
    sample = mongo.select(projection={'_id': 0, 'authors': 1}, limit=0)
    number = [0] * 30
    for doc in sample:
        authors = doc['authors']
        count = 0
        for author in authors:
            if 'id' in author.keys():
                count += 1
        number[count] += 1

    with open(paper_author_file, 'a', encoding='utf-8') as fw:
        for i in range(0, 30):
            text = "number:{} count:{}\n".format(i, number[i])
            fw.write(text)


def author_real_number(col):
    mongo = MongoProcess(collection=col)
    sample = mongo.select(projection={'_id': 0, 'authors': 1}, limit=0)
    number = [0] * 30
    with open(id_name_file, 'r', encoding='utf-8') as fw:
        toindex = json.load(fw)
    for doc in sample:
        authors = doc['authors']
        count = 0
        for author in authors:
            if 'id' in author.keys() and author['id'] in toindex.keys():
                count += 1
        number[count] += 1

    with open(paper_author_file, 'a', encoding='utf-8') as fw:
        for i in range(0, 30):
            text = "real_number:{} count:{}\n".format(i, number[i])
            fw.write(text)


def author_id():
    mongo = MongoProcess(collection='a_researcher')
    sample = mongo.select(projection={'_id': 0, 'id': 1, 'name': 1}, limit=0, sort=[('id', 1)])

    fw = open(author_id_file, 'a', encoding='utf-8')
    count = 0
    toindex = {}
    for doc in sample:
        id = doc['id']
        name = doc['name'].replace('\n', '')
        strs = '{}\t\t\t{}\t\t\t{}\n'.format(count, id, name)
        print(count)

        fw.write(strs)

        toindex[id] = count
        count += 1
    fw.close()

    with open(id_name_file, 'w', encoding='utf-8') as fw:
        json.dump(toindex, fw)


def dataset():
    mongo = MongoProcess(collection='a_paper')
    sample = mongo.select(projection={'_id': 0, 'authors': 1}, limit=0)
    for doc in sample:
        authors = doc['authors']
        count = 0
        ids = []
        names = []
        for author in authors:
            if 'id' in author.keys() and 'name' in author.keys():
                ids.append(author['id'])
                names.append(author['name'])
                count += 1

        if count >= 2:
            for i in range(count):
                for j in range(i + 1, count):
                    # add(i, j)
                    pass

    with open(table_data_file, 'w', encoding='utf-8') as fw:
        json.dump(dataset, fw)


if __name__ == '__main__':
    print('start data count')
    data_count()
    # print('start author number')
    # author_number('a_paper')
    # dataset()
    # author_id()
    # author_number('a_paper')
    # author_real_number('a_paper')
    # mongo = MongoProcess(collection='a_researcher')
    # mongo.ratio_coverage()
