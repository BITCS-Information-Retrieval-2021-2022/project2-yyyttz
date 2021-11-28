# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScholarAuthorItem(scrapy.Item):
    id = scrapy.Field()  # 学者ID
    name = scrapy.Field()  # 姓名
    indices_pubs = scrapy.Field()  # 发表文章数量
    indices_hindex = scrapy.Field()  # h指数
    indices_citations = scrapy.Field()  # 被引量
    profile_affiliation = scrapy.Field()  # 隶属(list)
    profile_homepage = scrapy.Field()  # 个人主页
    publications = scrapy.Field()  # 发表文章(list)

    highly_influential_citations = scrapy.Field()
    externalIds = scrapy.Field()  # (dict)
    aliases = scrapy.Field()  # 别名(list)


class ScholarPaperItem(scrapy.Item):
    id = scrapy.Field()  # 论文ID
    externalIds = scrapy.Field()  # "ArXiv"/"DBLP"等等(dict)
    year = scrapy.Field()  # 提交/发表年
    title = scrapy.Field()  # 标题
    abstract = scrapy.Field()  # 摘要
    authors = scrapy.Field()  # 作者(list)
    venue_info_name = scrapy.Field()  # 会议期刊名
    num_citation = scrapy.Field()  # 引用数

    num_reference = scrapy.Field()  # 参考数
    num_influentialCitation = scrapy.Field()  # 高引用数
    fieldsOfStudy = scrapy.Field()  # 领域类别
    references = scrapy.Field()  # 参考(list)