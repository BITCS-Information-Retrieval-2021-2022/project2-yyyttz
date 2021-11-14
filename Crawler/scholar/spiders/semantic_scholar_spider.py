import scrapy
import json
from scrapy import Request
from scholar.items import ScholarPaperItem, ScholarAuthorItem
from pymongo import MongoClient
import string

Count = 0


class ConnectMongoDB(object):
    def __init__(self):
        self.client = MongoClient(host='121.5.169.182', port=27017, username='ccty', password='asdfghjkl')
        self.database = self.client.IR

    def insert_author(self, author):
        collection_author = self.database.scholarAuthor
        collection_author.update({'id': author['id']}, {'$set': author.__dict__}, True)
        # one_result = collection_author.count_documents({"id": author['id']})
        # if one_result < 1:
        #     collection_author.insert_one(author.__dict__)
        #     global Count
        #     Count = Count + 1
        #     if Count == 50:
        #         print(
        #             "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #         return
        # writer = open("author.txt", "a+")
        # print(author['name'], file=writer)

    def insert_paper(self, paper):
        collection_paper = self.database.scholarPaper
        collection_paper.update({'id': paper['id']}, {'$set': paper.__dict__}, True)
        # one_result = collection_paper.count_documents({"id": paper['id']})
        # if one_result < 1:
        #     collection_paper.insert_one(paper.__dict__)


class SemanticScholarSpider(scrapy.Spider):
    name = "semanticscholar"
    allowed_domains = ["semanticscholar.org"]
    # start_urls = ["https://www.semanticscholar.org/author/Kashyap-Patel/1917579186"]
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
    db = ConnectMongoDB()

    def start_requests(self):
        line_list = []
        with open("start_url.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line[:-1]
                line_list.append(line)

        for start_url in line_list:
            yield scrapy.FormRequest(
                start_url,
                # cookies=self.cookies,
                # headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):
        this_url = response.url
        back_url_index = this_url.find('/author/')
        back_url = this_url[back_url_index + 8:]
        back_url = back_url.split('/')

        url_list = [url.root for url in response.xpath("//*/@href")]
        for url in url_list:
            if url.startswith('/author/') and url != this_url[back_url_index:]:
                yield Request("https://www.semanticscholar.org" + url, callback=self.parse)

        author = ScholarAuthorItem()
        # author = {}
        author['id'] = back_url[-1]
        author['name'] = back_url[-2]
        raw_data = response.xpath('//div[@class="author-detail-card__stats-row"]/span')

        author['indices_pubs'] = raw_data[1].root.text.replace(",", "")
        author['indices_hindex'] = raw_data[3].root.text.replace(",", "")
        author['indices_citations'] = raw_data[5].root.text.replace(",", "")
        author['highly_influential_citations'] = raw_data[7].root.text.replace(",", "")
        author["externalIds"] = None
        author["aliases"] = None
        author["profile_affiliation"] = None
        author["profile_homepage"] = None
        author["publications"] = None

        yield Request("https://api.semanticscholar.org/graph/v1/author/" + back_url[
            -1] + "?fields=url,externalIds,name,aliases,affiliations,homepage,papers",
                      meta={'item': author}, callback=self.parse_author_detail)

        for idx in range(0, int(float(author['indices_pubs'])), 20):
            yield Request("https://api.semanticscholar.org/graph/v1/author/" + back_url[
                -1] + "/papers?fields=externalIds,title,abstract,venue,year,authors.authorId,references.paperId,referenceCount,citationCount,influentialCitationCount,fieldsOfStudy&limit=20&offset=" + str(
                idx), callback=self.parse_pubs)

        yield author

    def parse_author_detail(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        author = response.meta["item"]
        try:
            author["externalIds"] = data["externalIds"] if data["externalIds"] else None
            author["aliases"] = data["aliases"] if data["aliases"] else None
            author["profile_affiliation"] = data["affiliations"] if data["affiliations"] else None
            author["profile_homepage"] = data["homepage"] if data["homepage"] else None
            author["publications"] = data["papers"] if data["papers"] else None
            # db = ConnectMongoDB()
            self.db.insert_author(author)
            yield author
        except KeyError:
            print("##########")
            print(data)
            print("Catch an exception!！")

    def parse_pubs(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        try:
            pubs = data["data"]
            for pub in pubs:
                item = ScholarPaperItem()
                item["id"] = pub["paperId"]
                item["externalIds"] = pub["externalIds"] if pub["externalIds"] else None
                item["title"] = pub["title"] if pub["title"] else None
                item["abstract"] = pub["abstract"] if pub["abstract"] else None
                item["venue_info_name"] = pub["venue"] if pub["venue"] else None
                item["year"] = pub["year"] if pub["year"] else None
                item["num_citation"] = pub['citationCount'] if pub['citationCount'] else None
                item["authors"] = pub['authors'] if pub['authors'] else None

                item["num_reference"] = pub["referenceCount"] if pub["referenceCount"] else None
                item["num_influentialCitation"] = pub["influentialCitationCount"] if pub[
                    "influentialCitationCount"] else None
                item["fieldsOfStudy"] = pub["fieldsOfStudy"] if pub["fieldsOfStudy"] else None
                item["references"] = pub["references"] if pub["references"] else None
                self.db.insert_paper(item)
                yield item
        except KeyError:
            print("!!!!!!!!!!")
            print(data)
            print("Catch an exception!")
