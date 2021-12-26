from elasticsearch import Elasticsearch
es = Elasticsearch()
if not es.ping():
    raise Exception("请打开ES")
for item in [
    "uer-simcse-base-chinese-none-0-data-origin.csv",
    "uer-sbert-base-chinese-nli-none-0-data-origin.csv",
    "sentence-transformers-paraphrase-multilingual-mpnet-base-v2-none-0-data-origin.csv"
]:
    es.indices.delete(item)
