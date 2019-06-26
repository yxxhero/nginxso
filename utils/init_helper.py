#!/usr/bin/env python3
from utils.elasticsearch_helper import ElasticSearch
from utils.config import get_config
from utils.log_helper import logger


class BaseInit(object):
    def __init__(self):
        self.keyword_map = {
            "mappings": {
                "properties": {
                    "keyword": {"type": "text"},
                    "module_name": {"type": "text"},
                }
            }
        }
        self.direct_retain_keyword = [
            "endpoints",
            "arguments",
            "summary",
            "issues",
            "example",
            "directives",
            "compatibility",
            "definitions",
            "protocol",
            "variables",
            "commands",
            "data",
            "compatibility",
            "properties",
        ]

        self.module_map = {
            "mappings": {
                "properties": {
                    "module_name": {"type": "text"},
                    "compatibility": {"type": "text"},
                    "properties": {"type": "text"},
                    "arguments": {"type": "text"},
                    "definitions": {"type": "text"},
                    "protocol": {"type": "text"},
                    "commands": {"type": "text"},
                    "data": {"type": "text"},
                    "summary": {"type": "text"},
                    "variables": {"type": "object"},
                    "issues": {"type": "text"},
                    "example": {"type": "text"},
                    "endpoints": {"type": "nested"},
                    "directives": {"type": "text"},
                    "directive_info": {"type": "nested"},
                }
            }
        }
        logger.info("初始化es实例")
        self.es_ins = ElasticSearch(
            ips=get_config("elasticsearch", "ips"),
            port=get_config("elasticsearch", "port"),
        )

    def es_index_init(self):

        # 创建es索引
        self.es_ins.create_index("keyword", self.keyword_map)
        self.es_ins.create_index("module", self.module_map)
