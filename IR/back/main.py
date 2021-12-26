from flask import Flask
from search import getList, searchInfor, searchRelation
import json

app = Flask(__name__)


@app.route('/query', methods=['GET'])
def search():
    res = getList()
    if res is not None:
        print("返回结果：", len(res))

    return json.dumps(res)


@app.route('/find', methods=['GET'])
def find():
    res = searchInfor()
    if res is not None:
        print("返回结果：", len(res))

    return json.dumps(res)


@app.route('/relation', methods=['GET'])
def relation():
    res = searchRelation()
    if res is not None:
        print("返回结果：", len(res))

    return json.dumps(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
