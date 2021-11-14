import scrapy
import json
import requests
from scrapy import Request
from scrapy.http import JsonRequest
import random

Count = 0


class PreprocessSpider(scrapy.Spider):
    name = "preprocess"
    allowed_domains = ["semanticscholar.org"]
    start_urls = "https://api.semanticscholar.org/graph/v1/author/"
    # login_url = "https://www.aminer.cn/login?callback="
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Host": "www.semanticscholar.org",
        "Accept-Encoding": "gzip, deflate, br",
    }
    cookies = {
        '_ga': 'GA1.2.1424061186.1635685406',
        '_gid': 'GA1.2.981072777.1635907402',
        '_gat_gtag_UA_67668211_2': '1',
        'gr_user_id': '9b5a984d-e923-4fa2-9951-c77567549785',
    }

    def start_requests(self):
        global Count
        id_list = []
        while Count < 500:
            temp_id = random.randint(1100000, 100000000)
            while temp_id in id_list:
                temp_id = random.randint(1100000, 100000000)
            url = self.start_urls + str(temp_id)
            yield scrapy.FormRequest(
                url,
                # cookies=self.cookies,
                # headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        if 'authorId' in data:
            global Count
            Count = Count + 1
            url = "https://www.semanticscholar.org/author/" + data['name'] + "/" + data['authorId']
            with open("start_url.txt", "a", encoding="utf-8") as f:
                print(url, file=f)
