import scrapy
import json
import pymongo
from scrapy import Request
from scrapy.http import JsonRequest
from scholar.items import AminerItem, PaperItem


class AminerSpider(scrapy.Spider):
    name = "aminer"
    allowed_domains = ["aminer.cn"]
    start_urls = [
        "https://www.aminer.cn/profile/ichiro-kawachi/54093048dabfae92b4260b4f",  # 历史
        "https://www.aminer.cn/profile/willem-van-mechelen/54350557dabfaebba5890321",  # 体育
        "https://www.aminer.cn/profile/gwo-jen-hwang/53f38029dabfae4b349f4abd",  # 教育
        "https://www.aminer.cn/profile/ed-diener/53f45fa4dabfaee0d9c14daa",  # 社会
        "https://www.aminer.cn/profile/david-b-audretsch/53f4bc23dabfaeda9d77b895",  # 经济管理
        "https://www.aminer.cn/profile/chi-tang-ho/5405b4eddabfae91d300449d",  # 食品
        "https://www.aminer.cn/profile/kurunthachalam-kannan/53f38e2bdabfae4b34a43c64",  # 环境
        "https://www.aminer.cn/profile/meinzer-frederick-c/563377c845cedb339aa1fb49",  # 林学
        "https://www.aminer.cn/profile/nanqi-ren/5448ee1ddabfaea4cf3c0bc4"  # 农业
        "https://www.aminer.cn/profile/meera-venkatesh/54488f17dabfae87b7e43018",  # 核
        "https://www.aminer.cn/profile/surendra-p-shah/53f7d354dabfae938c6e061c",  # 建筑
        "https://www.aminer.cn/profile/francesco-gesmundo/5435017edabfaebba588d68a",  # 冶金
        "https://www.aminer.cn/profile/nam-trung-nguyen/54489fcadabfae87b7e523e4",  # 仪器
        "https://www.aminer.cn/profile/robert-samuel-langer/53f4516bdabfaefedbb3e7e8",  # 生物 药学
        "https://www.aminer.cn/profile/daniel-r-weinberger/53f7a4c6dabfae9467da7bce",  # 神经
        "https://www.aminer.cn/profile/shizuo-akira/5488723bdabfae8a11fb435b",  # 免疫
        "https://www.aminer.cn/profile/stephen-v-faraone/548f1bdfdabfaef989f09791",  # 心理
        "https://www.aminer.cn/profile/walter-c-willett/5433f2aadabfaebba58314cf",  # 医学 临床
        "https://www.aminer.cn/profile/tasawar-hayat/54084a33dabfae450f408b17",  # 机械
        "https://www.aminer.cn/profile/mccartt-anne-t/563335e245cedb339a84d16c",  # 交通
        "https://www.aminer.cn/profile/harold-vincent-poor/54055927dabfae8faa5c5dfa",  # 电气
        "https://www.aminer.cn/profile/carlos-guedes-soares/540549a0dabfae92b41beb54",  # 海洋
        "https://www.aminer.cn/profile/xiangfang-li/542deee0dabfae48d12422a5",  # 石油
        "https://www.aminer.cn/profile/michael-a-carpenter/53f4756edabfaee2a1dea3a4",  # 矿业
        "https://www.aminer.cn/profile/kenji-ishihara/5440e64bdabfae805a70719c",  # 地质
        "https://www.aminer.cn/profile/julian-a-dowdeswell/54327833dabfaeb5421564e4",  # 地球
        "https://www.aminer.cn/profile/mingguo-zhai/56cb1897c35f4f3c65653560",  # 地质
        "https://www.aminer.cn/profile/xia-li/542a06dedabfaec7081d6431",  # 地理
        "https://www.aminer.cn/profile/wen-bao/53f45fd8dabfaee02ad7ac50",  # 航天
        "https://www.aminer.cn/profile/roberto-maiolino/548719c2dabfae8a11fb3604",  # 天文
        "https://www.aminer.cn/profile/guido-kroemer/548d00c5dabfae9b40135631",  # 生物
        "https://www.aminer.cn/profile/lihong-wang/54860d90dabfae8a11fb2f31",  # 光
        "https://www.aminer.cn/profile/shaojun-dong/548a2b2fdabfae9b40134f56",  # 化学
        "https://www.aminer.cn/profile/zhonglin-wang/542ec5bbdabfae498ae3ae6b",  # 物理
        "https://www.aminer.cn/profile/zeshui-xu/53f7f8bcdabfae90ec133088",  # 数学
        "https://www.aminer.cn/profile/andrew-booth/54093882dabfae450f46bfa0",  # 通信
        "https://www.aminer.cn/profile/yoshua-bengio/53f4ba75dabfaed83977b7db",  # 计算机
        # "https://www.aminer.cn/profile/paul-m-ridker/560c42ee45cedb33974f0234",
    ]
    login_url = "https://www.aminer.cn/login?callback="
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent ": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Host": "api.aminer.cn",
        "Accept-Encoding": "gzip, deflate, br",
    }
    cookies = {
        'abflag': 'b',
        '_ga': 'GA1.2.1133063263.1633152472',
        '_Collect_UD': 'jSP9cmEQndR6mn_BZWb_F',
        'gr_user_id': '9b5a984d-e923-4fa2-9951-c77567549785',
        'UM_distinctid': '17ccbe37ba238f-0c960d252f44db-b7a1b38-13c680-17ccbe37ba311a5',
        '_Collect_ISNEW': '1638183458313',
        '_YS_userAccect': 'lX7OiHPlz2s2jXnp0ca1n',
        '_gid': 'GA1.2.1541925244.1638183458',
        'gr_session_id_ae8dfb99e5e4cda1': '9fd24f57-6f7f-4b9b-a1a0-72a320d0706d',
        'gr_session_id_ae8dfb99e5e4cda1_9fd24f57-6f7f-4b9b-a1a0-72a320d0706d': 'true',
        '_Collect_CU': '%7B%22data%22%3A%7B%22user%22%3A%7B%22id%22%3A%2260f'
        '670d94c775efc5de1eee6%22%2C%22name%22%3A%22%u94E0%20%u5EB7%22%2C%22username%22%'
        '3A%22kangkai1999@foxmail.com%22%2C%22avatar%22%3A%22//cravatar.cn/avatar/95cea25'
        'e08bf7a768ac253378fe5a317.png%3Fs%3D80%26r%3Dg%26d%3Dretro%22%2C%22email%22%3A%2'
        '2kangkai1999@foxmail.com%22%2C%22phone%22%3Anull%2C%22client_id%22%3Anull%2C%22cr'
        'eated_time%22%3A%222021-07-20T06%3A44%3A41.127Z%22%2C%22raw_info%22%3A%7B%22addr%'
        '22%3A%22%22%2C%22gender%22%3A1%2C%22org%22%3A%22%22%2C%22src%22%3A%22aminer%22%2C'
        '%22sub%22%3Afalse%2C%22sub_email%22%3A%22kangkai1999@foxmai.com%22%2C%22title%22%3'
        'A%22Master%20Student%22%7D%7D%2C%22roles%22%3A%7B%22god%22%3Afalse%2C%22admin%22%3'
        'Afalse%2C%22authed%22%3Afalse%2C%22systems%22%3A%5B%5D%2C%22role%22%3A%5B%5D%2C%22'
        'authority%22%3A%5B%5D%2C%22primary%22%3Afalse%2C%22intermediate%22%3Afalse%2C%22se'
        'nior%22%3Afalse%2C%22forbid%22%3Afalse%2C%22bianyigetoken%22%3Afalse%7D%7D%2C%22tim'
        'e%22%3A1638192042529%7D',
        '_Collect_SN': '112'
    }

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.FormRequest(
                start_url,
                # headers=self.headers,
                # cookies=self.cookies,
                callback=self.parse
            )

    def parse(self, response):
        # region json part
        raw_data = response.xpath("//script")[4].root.text
        data = raw_data.strip('; \n\t').split('window.g_initialProps = ')[-1]
        data = json.loads(data)

        item = AminerItem()
        if 'profile' not in data:
            return
        if 'profile' in data['profile']['profile']:
            profile = data['profile']['profile']
        else:
            profile = {}
        item['id'] = profile['id'] if 'id' in profile else None
        item['links'] = profile['links'] if 'links' in profile else None
        item['name'] = profile['name'] if 'name' in profile else None
        item['name_zh'] = profile['name_zh'] if 'name_zh' in profile else None
        item['tags'] = profile['tags'] if 'tags' in profile else None
        item['tags_score'] = profile['tags_score'] if 'tags_score' in profile else None
        if 'indices' in profile:
            indices = profile['indices']
        else:
            indices = {}
        item['indices_citations'] = indices['citations'] if 'citations' in indices else None
        item['indices_hindex'] = indices['hindex'] if 'hindex' in indices else None
        item['indices_pubs'] = indices['pubs'] if 'pubs' in indices else None
        if 'profile' in profile:
            profile_profile = profile['profile']
        else:
            profile_profile = {}
        item['profile_address'] = profile_profile['address'] if 'address' in profile_profile else None
        item['profile_affiliation'] = profile_profile['affiliation'] if 'affiliation' in profile_profile else None
        item['profile_biography'] = profile_profile['bio'] if 'bio' in profile_profile else None
        item['profile_educations'] = profile_profile['edu'] if 'edu' in profile_profile else None
        item['profile_email'] = profile_profile['email'] if 'email' in profile_profile else None
        item['profile_fax'] = profile_profile['fax'] if 'fax' in profile_profile else None
        item['profile_gender'] = profile_profile['gender'] if 'gender' in profile_profile else None
        item['profile_homepage'] = profile_profile['homepage'] if 'homepage' in profile_profile else None
        item['profile_organization'] = profile_profile['org'] if 'org' in profile_profile else None
        item['profile_phone'] = profile_profile['phone'] if 'phone' in profile_profile else None
        item['profile_position'] = profile_profile['position'] if 'position' in profile_profile else None
        item['profile_position_zh'] = profile_profile['position_zh'] if 'position_zh' in profile_profile else None
        item['profile_work'] = profile_profile['work'] if 'work' in profile_profile else None
        item['publications'] = None  # data['profile']['profilePubs']
        # endregion

        # region pubs part
        url = "https://apiv2.aminer.cn/magic?a=GetPersonPubs__person.GetPersonPubs___"
        if not item['indices_pubs']:
            item['indices_pubs'] = 0
        for idx in range(0, item['indices_pubs'], 10):
            post_data = [
                {
                    "action": "person.GetPersonPubs",
                    "parameters": {
                        "offset": idx,
                        "size": 10,
                        "sorts": ["!year"],
                        "ids":[response.url.split('/')[-1]],
                        "searchType":"all"
                    },
                    "schema":{
                        "publication": ["id", "year", "title", "title_zh", "abstract", "abstract_zh"]
                        + ["authors._id", "authors.name", "authors.name_zh", "num_citation"]
                        + ["venue.info.name", "venue.volume", "venue.info.name_zh", "venue.issue"]
                        + ["pages.start", "pages.end", "lang", "pdf", "doi", "urls", "versions"]
                    }
                }
            ]
            yield JsonRequest(url=url, headers=self.headers,
                              cookies=self.cookies, callback=self.parse_pubs, data=post_data)
        # endregion

        yield item
        print('=', end='')

    def parse_pubs(self, response):
        raw_data = json.loads(response.body.decode())
        if 'items' in raw_data['data'][0]:
            pubs = raw_data['data'][0]['items']
        else:
            return
        for pub in pubs:
            item = PaperItem()
            item['id'] = pub['id'] if 'id' in pub else None
            item['year'] = pub['year'] if 'year' in pub else None
            item['title'] = pub['title'] if 'title' in pub else None
            item['title_zh'] = pub['title_zh'] if 'title_zh' in pub else None
            item['abstract'] = pub['abstract'] if 'abstract' in pub else None
            item['abstract_zh'] = pub['abstract_zh'] if 'abstract_zh' in pub else None
            item['authors'] = pub['authors'] if 'authors' in pub else None
            item['order'] = pub['order'] if 'order' in pub else None
            item['num_citation'] = pub['num_citation'] if 'num_citation' in pub else None
            item['lang'] = pub['lang'] if 'lang' in pub else None
            item['pdf'] = pub['pdf'] if 'pdf' in pub else None
            item['doi'] = pub['doi'] if 'doi' in pub else None
            item['urls'] = pub['urls'] if 'urls' in pub else None
            item['versions'] = pub['versions'] if 'versions' in pub else None
            if 'venue' in pub:
                venue = pub['venue']
            else:
                venue = {}
            item['venue_issue'] = venue['issue'] if 'issue' in venue else None
            item['venue_volume'] = venue['volume'] if 'volume' in venue else None
            if 'info' in venue:
                info = venue['info']
            else:
                info = {}
            item['venue_info_name'] = info['name'] if 'name' in info else None
            item['venue_info_name_zh'] = info['name_zh'] if 'name_zh' in info else None
            if 'pages' in pub:
                pages = pub['pages']
            else:
                pages = {}
            item['pages_end'] = pages['end'] if 'end' in pages else None
            item['pages_start'] = pages['start'] if 'start' in pages else None
            for author in item['authors']:
                if 'id' not in author or 'name' not in author:
                    continue
                id = author['id']
                name = author['name'].replace('. ', '-').replace(' ', '-')
                yield Request("https://www.aminer.cn/profile/" + name + '/' + id, callback=self.parse)
            yield item
