from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

'''预处理，获取start_url列表'''
# execute(['scrapy', 'crawl', 'preprocess'])

'''爬虫'''
# execute(['scrapy', 'crawl', 'semanticscholar'])

execute(['scrapy', 'crawl', 'semanticscholarmodify'])
