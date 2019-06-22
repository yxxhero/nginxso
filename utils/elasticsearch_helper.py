import os
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from utils.log_helper import logger


class ElasticSearch(object):
    def __init__(self, index_name, index_type, ip, user_name=None, user_pass=None, port=9200):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        :param ip: a list of host 
        :param user_name: es用户名
        :param user_pass: es密码
        '''
        self.index_name = index_name
        self.index_type = index_type

        if all([user_name, user_pass]):
            self.es = Elasticsearch(ip, http_auth=(
                user_name, user_pass), port=port)
        else:
            self.es = Elasticsearch(ip, port)

    def create_index(self, index_name, index_type, map_body):

        # 创建映射
        # _index_mappings = {
        #     "mappings": {
        #         self.index_type: {
        #             "properties": {
        #                 "title": {
        #                     "type": "text",
        #                     "index": True,
        #                     "analyzer": "ik_max_word",
        #                     "search_analyzer": "ik_max_word"
        #                 },
        #                 "date": {
        #                     "type": "text",
        #                     "index": True
        #                 },
        #                 "keyword": {
        #                     "type": "string",
        #                     "index": "not_analyzed"
        #                 },
        #                 "source": {
        #                     "type": "string",
        #                     "index": "not_analyzed"
        #                 },
        #                 "link": {
        #                     "type": "string",
        #                     "index": "not_analyzed"
        #                 }
        #             }
        #         }

        #     }
        # }

        if not self.es.indices.exists(index=self.index_name):
            res = self.es.indices.create(
                index=self.index_name, body=map_body)
            logge.info(res)

    def insert_index_data(self, index_data):
        '''
        数据存储到es
        :return:
        '''
        for item in index_data:
            res = self.es.index(index=self.index_name,
                                doc_type=self.index_type, body=item)
            logger.info(res['created'])

    def bulk_insert_index_data(self, mul_index_data):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        ACTIONS = []
        for line in mul_index_data:
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_source": {
                    "date": line['date'],
                    "source": line['source'].decode('utf8'),
                    "link": line['link'],
                    "keyword": line['keyword'].decode('utf8'),
                    "title": line['title'].decode('utf8')}
            }
            ACTIONS.append(action)
            # 批量处理
        success, _ = bulk(self.es, ACTIONS,
                          index=self.index_name, raise_on_error=True)
        logger.info('Performed %d actions' % success)

    def delete_index_data(self, id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name,
                             doc_type=self.index_type, id=id)
        logger.info res

    def get_data_id(self, id):

        res = self.es.get(index=self.index_name,
                          doc_type=self.index_type, id=id)
        (res['_source'])

        logger.info '------------------------------------------------------------------'
        #
        # # 输出查询到的结果
        for hit in res['hits']['hits']:
            # logger.info hit['_source']
            logger.info hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], hit['_source']['title']

    def get_data_by_body(self):
        # doc = {'query': {'match_all': {}}}
        doc = {
            "query": {
                "match": {
                    "keyword": "电视"
                }
            }
        }
        _searched = self.es.search(
            index=self.index_name, doc_type=self.index_type, body=doc)

        for hit in _searched['hits']['hits']:
            # logger.info hit['_source']
            logger.info hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
                hit['_source']['title']
