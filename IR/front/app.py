import csv
from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
import json
import requests

app = Flask(__name__)


def getData(query, start, size):
    response = requests.get("http://121.5.169.182:5000/query?query={}&from={}&size={}".format(query, start, size))
    return response.content.decode("utf-8")


def getInformation(id, start2, size2):
    response = requests.get("http://121.5.169.182:5000/find?id={}&from={}&size={}".format(id, start2, size2))
    return response.content.decode("utf-8")


def getGraph(id):
    response = requests.get("http://121.5.169.182:5000/relation?id={}".format(id))
    return response.content.decode("utf-8")


query1 = ''
start = 0
size = 10
start2 = 0
size2 = 5


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global query1
        query1 = request.form.get('sentence')
        # answer = get_answer_normal(query)
        # answer = [['id','name','name_zh','indices_hindex','indices_pubs','职务级别','就职机构','研究兴趣','被引量']]
        return redirect(url_for('candidates'))
    return render_template('index.html')
    # return render_template('graph-force.html')


@app.route('/candidates', methods=['GET', 'POST'])
def candidates():
    page = 0
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        if (page < 0):
            page = 0
        elif (page > 10):
            page = 10
        global start
        start = page
    print('query1:', query1, 'start:', start)
    response = getData(query1, start, size)
    dataList = json.loads(response)
    print(dataList)
    tagstring = ''
    for j in range(len(dataList)):
        item = dataList[j]
        if item['tags'] is None:
            continue
        for i in range(len(item['tags'])):
            if(item['tags'][i]):
                tagstring = item['tags'][i] + ';' + tagstring
        dataList[j]['tagstring'] = tagstring
        tagstring = ''

    return render_template('candidates.html', pair=dataList, start=start, size=size)


@app.route('/browsejobs/<id>')
def browsejobs(id):
    page = 0
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        print('page:', page)
        if (page < 0):
            page = 0
        elif (page > 5):
            page = 5
        global start
        start = page
    response = getInformation(id, start2, 5)
    dataList = json.loads(response)
    dataList2 = getGraph(id)
    graphdataList = json.loads(dataList2)
    print('graphdataList', graphdataList)
    authorstring = ''
    print('dataList', dataList)
    for j in range(len(dataList['papers'])):
        item = dataList['papers'][j]
        for i in item['authors']:
            authorstring = i['name'] + ';' + authorstring
        dataList['papers'][j]['authorstrings'] = authorstring
        authorstring = ''
        print(dataList['papers'][j])

    return render_template(
        'browsejobs.html',
        pair=dataList['papers'],
        start=start2, size=size2,
        graphdataList=graphdataList,
        name_zh=dataList['name_zh'],
        name=dataList['name'],
        profile=dataList['profile_position'],
        jigou=dataList['profile_affiliation'],
        graph=[graphdataList]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
