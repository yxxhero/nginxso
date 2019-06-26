from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from utils.log_helper import logger
from utils.config import get_config


class ElasticSearch(object):
    def __init__(self, ips, port=9200, user_name=None, user_pass=None):
        """

        :param ip: a list of host
        :param user_name: es用户名
        :param user_pass: es密码
        """
        self.ips = ips.split(",")

        if all([user_name, user_pass]):
            self.es = Elasticsearch(
                self.ips, http_auth=(user_name, user_pass), port=port
            )
        else:
            self.es = Elasticsearch(self.ips, port=port)

    def create_index(self, index_name, map_body=None):

        if not self.es.indices.exists(index=index_name):
            if map_body:
                res = self.es.indices.create(index=index_name, body=map_body)
            else:
                res = self.es.indices.create(index=index_name)
            logger.info(res)

    def delete_index(self, index_name):

        # 删除索引
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
            logger.info("删除索引{}成功".format(index_name))

    def insert_one_index_data(self, index_name, index_data, index_type="_doc"):
        """
        数据存储到es
        :return:
        """
        res = self.es.index(index=index_name, doc_type=index_type, body=index_data)
        logger.info(res)

    def insert_mul_index_data(self, index_name, mul_index_data, index_type="_doc"):
        """
        用bulk将批量数据存储到es
        :return:
        """
        ACTIONS = []
        for line in mul_index_data:
            action = {"_index": index_name, "_type": index_type, "_source": line}
            ACTIONS.append(action)
        # 批量处理
        success, _ = bulk(self.es, ACTIONS, index=index_name, raise_on_error=True)
        logger.info("Performed %d actions" % success)

    def delete_index_data_by_id(self, index_name, id, index_type="_doc"):
        """
        删除索引中的一条
        :param id:
        :return:
        """
        res = self.es.delete(index=index_name, doc_type=index_type, id=id)
        logger.info(res)

    def delete_index_data_by_query(self, index_name, query_body):
        """
        删除query_body查询出的所有内容
        :param index_name: index_name
        :param index_type: index_type
        :param query_body: es query
        :return:
        """
        res = self.es.delete_by_query(index=index_name, body=query_body)
        logger.info(res)

    def get_data_by_id(self, index_name, id, index_type="_doc"):

        res = self.es.get(index=index_name, doc_type=index_type, id=id)

        logger.info(res["_source"])

        # 输出查询到的结果
        for hit in res["hits"]["hits"]:
            # logger.info hit['_source']
            logger.info(
                hit["_source"]["date"],
                hit["_source"]["source"],
                hit["_source"]["link"],
                hit["_source"]["keyword"],
                hit["_source"]["title"],
            )

    def get_data_by_body(self, index_name, query_body=None):
        if not query_body:
            query_body = {"query": {"match_all": {}}}
        return self.es.search(index=index_name, body=query_body)


if __name__ == "__main__":
    es_ins = ElasticSearch(
        "test",
        "test",
        get_config("elasticsearch", "ips"),
        get_config("elasticsearch", "port"),
    )
