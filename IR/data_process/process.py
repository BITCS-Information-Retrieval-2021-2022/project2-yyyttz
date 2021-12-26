# 静态数据库处理文件
from mongodb import MongoProcess
import re


# 将a_paper数据库导出为re_paper
# re_paper contains author_id and paper_id
def treat():
    paperMongo = MongoProcess(collection='a_paper')
    newMongo = MongoProcess(collection='re_paper1')

    sample = paperMongo.select(projection={'_id': 0}, limit=0)
    for doc in sample:
        authors = doc['authors']
        if authors is None:
            continue
        for author in authors:
            if 'id' in author.keys():
                result = {
                    'author_id': author['id'],
                    'paper_id': doc['id']
                }
                newMongo.insert([result])


# a_paper中id去重
def remove_duplicate_id():
    newMongo = MongoProcess(collection='a_paper')
    projection = {'_id': 1, 'id': 1}
    result = newMongo.select(projection=projection, limit=0, sort=[('id', -1)])

    last = ''
    count = 1
    for i in result:
        if i['id'] == last:
            newMongo.delete({'_id': i['_id']})
            continue
        last = i['id']
        print('正在处理第{}个数据'.format(count))
        count += 1


# 建立两个作者共同发表论文数
def author_edge():
    mongo = MongoProcess(collection='a_paper')
    sample = mongo.select(projection={'_id': 0, 'authors': 1}, limit=0)

    for doc in sample:
        authors = doc['authors']
        ids = []
        for author in authors:
            if 'id' in author.keys():
                ids.append(author['id'])

        print(len(ids))
        if len(ids) >= 2:
            for i in range(0, len(ids)):
                for j in range(i, len(ids)):
                    insert(ids[i], ids[j])


def insert(idx, idy):
    if idx > idy:
        temp = idx
        idx = idy
        idy = temp

    author_relation = MongoProcess(collection='author_relation')
    filter = {'author_x': idx, 'author_y': idy}
    check = author_relation.select_one(filter=filter)

    if check is None:
        data = {'author_x': idx, 'author_y': idy, 'papers': 1}
        author_relation.insert([data])
    else:
        papers = check['papers'] + 1
        update = {'papers': papers}
        author_relation.update_one(filter, update)


# 得到同一个名字的id列表
def tong_ming():
    mongo = MongoProcess(collection='a_researcher')
    newMongo = MongoProcess(collection='author_name')
    sample = mongo.select(projection={'_id': 0, 'id': 1, 'name': 1}, limit=0)

    for doc in sample:
        doc['name'] = doc['name'].replace('-', '').replace('_', '').strip().lower()
        name = re.sub(r"\s\s+", " ", doc['name'])
        res = newMongo.select_one(filter={'name': name})

        print(name)
        if res is None:
            data = {
                'name': name,
                'ids': [doc['id']]
            }
            newMongo.insert([data])
        else:
            ids = res['ids']
            ids.append(doc['id'])
            newMongo.update_one({'name': name}, {'ids': ids})


# 得到tag对应的id列表
def tags_id():
    mongo = MongoProcess(collection='a_researcher')
    newMongo = MongoProcess(collection='tag_author')
    sample = mongo.select(projection={'_id': 0, 'id': 1, 'tags': 1}, limit=0)

    for doc in sample:
        tags = doc['tags'] if doc['tags'] else []
        for tag in tags:
            res = newMongo.select_one(filter={'tag': tag})
            print(tag)
            if res is None:
                data = {
                    'tag': tag,
                    'ids': [doc['id']]
                }
                newMongo.insert([data])
            else:
                ids = res['ids']
                ids.append(doc['id'])
                newMongo.update_one({'tag': tag}, {'ids': ids})


if __name__ == '__main__':
    tong_ming()
