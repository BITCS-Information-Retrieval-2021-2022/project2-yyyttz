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


class AminerItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # 学者ID
    indices_citations = scrapy.Field()  # 被引量
    indices_hindex = scrapy.Field()  # h指数
    indices_gindex = scrapy.Field()  # g指数
    indices_pubs = scrapy.Field()  # 发表数
    links = scrapy.Field()  # 资料链接(list)
    name = scrapy.Field()  # 姓名
    name_zh = scrapy.Field()  # 中文姓名
    profile_address = scrapy.Field()  # 地址
    profile_affiliation = scrapy.Field()  # 就职机构
    profile_biography = scrapy.Field()  # 个人简介
    profile_educations = scrapy.Field()  # 教育背景
    profile_email = scrapy.Field()  # 电子邮箱
    profile_fax = scrapy.Field()  # 传真
    profile_gender = scrapy.Field()  # 性别
    profile_homepage = scrapy.Field()  # 个人主页
    profile_organization = scrapy.Field()  # 组织
    profile_phone = scrapy.Field()  # 电话
    profile_position = scrapy.Field()  # 职务级别
    profile_position_zh = scrapy.Field()  # 中文职务级别
    profile_work = scrapy.Field()  # 工作经历
    tags = scrapy.Field()  # 研究兴趣
    tags_score = scrapy.Field()  # 研究兴趣指数
    publications = scrapy.Field()  # 发表文章(list)


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # 论文ID
    year = scrapy.Field()  # 提交/发表年
    title = scrapy.Field()  # 标题
    title_zh = scrapy.Field()  # 中文标题
    abstract = scrapy.Field()  # 摘要
    abstract_zh = scrapy.Field()  # 中文摘要
    authors = scrapy.Field()  # 作者(list)(id, name, name_zn)
    order = scrapy.Field()  # ??
    num_citation = scrapy.Field()  # 引用数
    venue_issue = scrapy.Field()  # ?? 子会子刊
    venue_volume = scrapy.Field()  # 会议期刊卷
    venue_info_name = scrapy.Field()  # 会议期刊名
    venue_info_name_zh = scrapy.Field()  # 会议期刊中文名
    pages_end = scrapy.Field()  # 终止页
    pages_start = scrapy.Field()  # 起始页
    lang = scrapy.Field()  # 语言
    pdf = scrapy.Field()  # PDF地址
    doi = scrapy.Field()  # DOI
    urls = scrapy.Field()  # URL(list)
    versions = scrapy.Field()  # 版本(list)
