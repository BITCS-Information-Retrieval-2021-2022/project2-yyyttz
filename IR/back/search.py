from flask import request
import tqdm
import csv
from elasticsearch import Elasticsearch
import os
import math
import argparse
from mongodb import MongoProcess

es = Elasticsearch()


def get_query():
    res = {}
    args = request.args
    for key in args:
        res[key] = args[key]
    reformat_title(res)

    return res


def reformat_title(args):
    args["from"] = int(args["from"])
    args["size"] = int(args["size"])
    args["index"] = None


def getList():
    query = get_query()

    index = "aminer_researcher"
    query["index"] = "name"
    hit1 = search_author(index, query)
    query["index"] = "name_zh"
    hit2 = search_author(index, query)
    query["index"] = "ac"
    hit3 = search_author(index, query)
    # index = "a_paper"
    # query["index"] = "title"
    # hit4 = search_author(index, query)
    index = "tag_author"
    query["index"] = "tag"
    hit5 = search_author(index, query)

    # compare
    score = []
    if hit1['hits']['max_score'] is not None:
        score.append(hit1['hits']['max_score'])
    if hit2['hits']['max_score'] is not None:
        score.append(hit2['hits']['max_score'])
    if hit3['hits']['max_score'] is not None:
        score.append(hit3['hits']['max_score'])
    # if hit4['hits']['max_score'] is not None:
        # score.append(hit4['hits']['max_score'])
    if hit5['hits']['max_score'] is not None:
        score.append(hit5['hits']['max_score'])

    if len(score) == 0:
        return []

    maxinum = max(score)
    number = 0
    if hit1['hits']['max_score'] is not None and maxinum == hit1['hits']['max_score']:
        hit = hit1
        number = 1
        collection = 'a_researcher'
    elif hit2['hits']['max_score'] is not None and maxinum == hit2['hits']['max_score']:
        number = 2
        hit = hit2
        collection = 'a_researcher'
    elif hit3['hits']['max_score'] is not None and maxinum == hit3['hits']['max_score']:
        number = 3
        hit = hit3
        collection = 'a_researcher'
    # elif hit4['hits']['max_score'] is not None and maxinum == hit4['hits']['max_score']:
    #     number = 4
    #     hit = hit4
    #     collection = 'a_paper'
    else:
        number = 5
        hit = hit5
        collection = 'tag_author'
    print('hit1', hit1)
    print('hit2', hit2)
    print('hit3', hit3)
    # print('hit4', hit4)
    print('hit5', hit5)
    print('maxinum', maxinum, 'number', number, score)

    if collection == 'tag_author':
        mongo = MongoProcess(collection='tag_author')
        print(hit['hits']['hits'])
        res = mongo.select_one(filter={'tag': hit['hits']['hits'][0]['_source']['tag']})
        id_list = res['ids']

        mongo = MongoProcess(collection='a_researcher')
        res = mongo.select(filter={'id': {'$in': id_list}}, limit=0)

        result = [doc for doc in res]
        res = sorted(result, key=lambda d: d['indices_hindex'] + math.log10(d['indices_citations'] + 1), reverse=True)
    else:
        mongo = MongoProcess(collection=collection)
        res = mongo.search_by_id_list(hit['id_list'])

    if number != 1 and number != 2:
        result = sorted(res, key=lambda d: d['indices_hindex'] + math.log10(d['indices_citations'] + 1), reverse=True)
        res = result

    return res


def searchInfor():
    args = request.args
    id = args['id']

    mongo = MongoProcess(collection='a_researcher')
    res = mongo.search_by_id(id)
    if res is None:
        return {}

    query = get_query()
    hit = search_paper(query)
    print('hit::::', hit)
    mongo = MongoProcess(collection='a_paper')
    papers = mongo.search_by_id_list(hit['id_list'])

    res['papers'] = papers

    return res


def searchRelation():
    args = request.args
    query = {
        'id': args['id']
    }
    body = {
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {"match": {"author_x": query["id"]}},
                            {"match": {"author_y": query["id"]}}
                        ]
                    }
                }
            }
        }
    }
    # 字符检索
    res = es.search(index='author_relation', body=body)

    points = [item['_source'] for item in res['hits']['hits']]
    res = []
    for i in points:
        if i['author_x'] == query['id'] and i['author_y'] == query['id']:
            continue
        if i['author_x'] == query['id']:
            object = i['author_y']
        else:
            object = i['author_x']

        mongo = MongoProcess(collection='a_researcher')
        data = mongo.search_by_id(object)
        if data is not None:
            res.append({
                'id': object,
                'name': data['name'],
                'papers': i['papers']
            })

    if len(res) == 0:
        return []
    angle = 2 * math.pi / len(res)
    output = [{
        'author_id': query['id'],
        'name': '_',
        'papers': 0,
        'x': 0,
        'y': 0
    }]
    links = [{
        'source': '_',
        'target': '_',
        'distance': 0
    }]
    maxinum = max([math.log2(r['papers'] + 1) for r in res])
    for i in range(len(res)):
        distance = round(5 / (math.log2(res[i]['papers'] + 1)))
        distance = round(maxinum + 2 - math.log2(res[i]['papers'] + 1), 2)
        x = distance * math.cos(i * angle)
        y = distance * math.sin(i * angle)
        output.append({
            'author_id': res[i]['id'],
            'name': res[i]['name'],
            'papers': res[i]['papers'],
            'x': x,
            'y': y
        })

        a = {
            "source": "_",
            "target": res[i]['name'],
            "distance": distance
        }
        print(a)
        links.append(a)

    result = {
        "nodes": output,
        "links": links
    }

    return result


def search_author(index, query):
    es_query = {
        "track_total_hits": "true",
        "from": query["size"] * query["from"],
        "size": query["size"],
        "query": {
            "bool": {
                "must": [
                    {
                        "function_score": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                query['index']: {
                                                    "query": query["query"],
                                                    "boost": 2.0,
                                                    "operator": "or"
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                            "functions": [
                                {
                                    "field_value_factor": {
                                        "field": "importance",
                                        "modifier": "log1p",
                                        "missing": 1
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }

    # body = {
    #     "query": {
    #         "match": {
    #             query['index']: query['query']
    #         }
    #     },
    #     "from": query['from'],
    #     "size": query['size']
    # }
    # 字符检索
    res = es.search(index=index, body=es_query)

    try:
        id_list = [item['_source']['id'] for item in res['hits']['hits']]
    except Exception:
        id_list = []
    res['id_list'] = id_list

    return res


def search_paper(query):
    body = {
        "query": {
            "match": {
                'author_id': query['id']
            }
        },
        "from": query['from'],
        "size": query['size']
    }
    # 字符检索
    res = es.search(index='re_paper', body=body)

    id_list = [item['_source']['paper_id'] for item in res['hits']['hits']]
    res['id_list'] = id_list

    return res
